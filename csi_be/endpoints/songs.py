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

import logging

# Get logger
logger = logging.getLogger(__name__)
# Create a handler
c_handler = logging.StreamHandler()
# link handler to logger
logger.addHandler(c_handler)
# Set logging level to the logger
logger.setLevel(logging.DEBUG) # <-- THIS!


@app.route("/songs/count", methods=['GET'])
def get_song_count():
    return db.songs.count_documents(), 200

@app.route("/songs/<id>")
def get_song(id):
    """Song schema:
    {
        "_id": "ObjectId",
        "title": "string",
        "upload_date": datatime,
        "embeddings": npz,
        "features": {
            "hpcp": npz,
            "mfcc": npz
        },
        "version": 1.0
    }

    Args:
        id (str): id of song in mongo

    Returns:
        JSON: the song
    """
    logger.info("Received request to get_song")
    return db.songs.find({'_id': id}), 200

@app.route("/songs", methods=['GET', 'POST'])
def songs():
    request_id = str(uuid4())
    tmp_path = config.DATA_DIR + "/" + request_id
    if request.method == 'GET':
        """Return all songs

        Returns:
            list of songs
        """
        logger.info("Received request to list all songs")
        docs = db.songs.find({})
        dtos = [convert_song_doc_to_dto(doc) for doc in docs]
        return dtos, 200
    elif request.method == 'POST':
        """Upload schema:
        {
            "yt_link": string
        }

        Returns:
            str: response
        """
        try:
            os.makedirs(tmp_path)
            logger.info(f"tmp path: {tmp_path}")
            dto = request.get_json()
            
            res = db.songs.find_one({'yt_link': dto['yt_link']})
            if res is not None:
                return convert_song_doc_to_dto(res), 200
            
            # Download song
            print("Downloading song")
            downloader.download(tmp_path, dto['yt_link'])
            
            # Generate features
            print("Generating features")
            entry = os.listdir(tmp_path)[0]
            features = feature_extractor.extract(os.path.join(tmp_path, entry))
            title = entry.split('.')[0]
            hpcp_pickle = bson.binary.Binary( pickle.dumps(features, protocol=2) )
            
            # Generate embeddings
            print("Generating embeddings")
            emb = inferencer.generate_embeddings(features)
            emb_pickle = bson.binary.Binary( pickle.dumps(emb, protocol=2) )
        
            doc = {}
            doc['title'] = title
            doc['upload_date'] = datetime.now()
            doc['features'] = {
                'hpcp': hpcp_pickle
            }
            doc['version'] = config.APP_VERSION
            doc['embeddings'] = emb_pickle
            doc['yt_link'] = dto['yt_link']
            
            print("Saved to database")
            db.songs.insert_one(doc)
            
            doc = db.songs.find_one({'yt_link': dto['yt_link']})
            return convert_song_doc_to_dto(doc), 200
        except Exception as e:
            return str(e), 500
        finally:
            shutil.rmtree(tmp_path)
        