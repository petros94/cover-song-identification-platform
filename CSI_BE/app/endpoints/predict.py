from datetime import datetime
import os
import pymongo
import pickle
from app import app, db, downloader, feature_extractor, inferencer
from endpoints.converters import convert_song_doc_to_dto, convert_song_doc_to_dto_with_dist, convert_song_doc_to_dto_with_dist_cover
from config import config
from storage import download_blob
from flask import request
from uuid import uuid4
import numpy as np
import shutil
import logging
import bson
import torch
from bson.objectid import ObjectId

import logging

# Get logger
logger = logging.getLogger(__name__)
# Create a handler
c_handler = logging.StreamHandler()
# link handler to logger
logger.addHandler(c_handler)
# Set logging level to the logger
logger.setLevel(logging.DEBUG) # <-- THIS!

def gen_embeddings(doc, segment=True):
    if float(doc['version']) < float(config.APP_VERSION):
        logger.info(f"Generating new embeddings for {doc['title']}")
        blob = download_blob(str(doc['_id']))
        features = pickle.loads(blob)
        emb = inferencer.generate_embeddings(features, segment=False)
        emb_seg = inferencer.generate_embeddings(features, segment=True)
        newvalues = { "$set": { 
            'embeddings': bson.binary.Binary( pickle.dumps(emb.numpy(), protocol=2) ),
            'embeddings_seg': bson.binary.Binary( pickle.dumps(emb_seg.numpy(), protocol=2) ),
            'version': config.APP_VERSION
            } }
        db.songs.update_one({'_id': doc['_id']}, newvalues)
        logger.info("Updated embeddings")
    else:
        emb = torch.tensor(pickle.loads(doc['embeddings']))
        emb_seg = torch.tensor(pickle.loads(doc['embeddings_seg']))
        logger.info("Loaded precomputed embeddings")
    return emb_seg if segment else emb

@app.route("/predict/pair", methods=['GET'])
def predict_pair():
    song_id_1 = request.args['id_1']
    song_id_2 = request.args['id_2']
    
    doc_1 = db.songs.find_one({'_id': ObjectId(song_id_1)})
    doc_2 = db.songs.find_one({'_id': ObjectId(song_id_2)})
        
    emb_1 = gen_embeddings(doc_1)
    emb_2 = gen_embeddings(doc_2)
    
    # Find minimum length
    min_len = min(len(emb_1), len(emb_2))

    # Crop to minimum length
    emb_1 = emb_1[: min_len]
    emb_2 = emb_2[: min_len]
    
    is_cover, dist, is_cover_mean = inferencer.predict(emb_1, emb_2)
    return {'is_cover': is_cover_mean, 
            'dist': np.mean(dist.tolist()),
            'is_cover_segments': is_cover.tolist(),
            'dist_segments': dist.tolist()}, 200
    
    
@app.route("/predict/rank", methods=['GET'])
def predict_rank():
    song_id= request.args['id_1']
    
    doc_1 = db.songs.find_one({'_id': ObjectId(song_id)})
    emb_1 = gen_embeddings(doc_1, segment=False)
    
    docs = db.songs.find({})
    embeddings = []
    dtos = []
    for doc in docs:
        emb = gen_embeddings(doc, segment=False)
        embeddings.append(emb)
        dtos.append(doc)
    embeddings = torch.cat(embeddings, dim=0)
    
    logger.info("Calculating distances")
    distances = torch.cdist(emb_1, embeddings).squeeze(0).numpy()
    inv = 2 - distances
    covers = ((inv > inferencer.D_full)*1).tolist()
    
    ids = np.argsort(distances)
    embeddings = embeddings.tolist()
    
    return [convert_song_doc_to_dto_with_dist_cover(dtos[i], distances[i], embeddings[i], covers[i]) for i in ids]
    
    
@app.route("/predict/rankaggregated", methods=['GET'])
def predict_rank_aggregated():
    song_id= request.args['id_1']
    
    doc_1 = db.songs.find_one({'_id': ObjectId(song_id)})
    anchor = gen_embeddings(doc_1)
    
    docs = db.songs.find({})
    distances = []
    embeddings = []
    covers = []
    dtos = []
    for doc in docs:
        emb = gen_embeddings(doc)
        
        # Find minimum length
        min_len = min(len(anchor), len(emb))

        # Crop to minimum length
        emb_1 = anchor[: min_len]
        emb_2 = emb[: min_len]
        
        _, dist, is_cover_mean = inferencer.predict(emb_1, emb_2)
        
        dist = np.mean(dist.tolist())
        
        distances.append(dist if not np.isnan(dist) else 1.00)
        covers.append(is_cover_mean)
        dtos.append(doc)
        embeddings.append(torch.mean(emb_2, dim=-1))
        
    embeddings = torch.cat(embeddings, dim=0).tolist()
    ids = np.argsort(distances)  
    return [convert_song_doc_to_dto_with_dist_cover(dtos[i], distances[i], embeddings[i], covers[i]) for i in ids]