from datetime import datetime
import os
import pymongo
import pickle
from app import app, db, downloader, feature_extractor, inferencer
from endpoints.converters import convert_song_doc_to_dto
from config import config
from flask import request
from uuid import uuid4
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


@app.route("/predict/pair", methods=['GET'])
def predict_pair():
    song_id_1 = request.args['id_1']
    song_id_2 = request.args['id_2']
    
    doc_1 = db.songs.find_one({'_id': ObjectId(song_id_1)})
    doc_2 = db.songs.find_one({'_id': ObjectId(song_id_2)})
    
    emb_1 = torch.tensor(pickle.loads(doc_1['embeddings'])).unsqueeze(0)
    emb_2 = torch.tensor(pickle.loads(doc_2['embeddings'])).unsqueeze(0)
    
    is_cover, dist = inferencer.predict(emb_1, emb_2)
    return {'is_cover': is_cover.tolist()[0], 'dist': dist.tolist()[0]}, 200
    
    
    