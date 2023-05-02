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

def gen_live_embeddings(tmp_path, segment=True):
    entry = os.listdir(tmp_path)[0]
    features = feature_extractor.extract(os.path.join(tmp_path, entry))
    if segment:
        return inferencer.generate_embeddings(features, segment=True)
    else:
        return inferencer.generate_embeddings(features, segment=False)
    
@app.route("/live", methods=['POST'])
def predict_rank_aggregated():
    files = request.files
    file = files.get('file')
    request_id = str(uuid4())
    tmp_path = config.DATA_DIR + "/" + request_id
    os.makedirs(tmp_path)
    with open(tmp_path + '/temp', 'wb') as f:
        f.write(file.content)
        
    anchor = gen_live_embeddings(tmp_path)
    
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