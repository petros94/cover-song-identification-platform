from datetime import datetime
import os
import pymongo
import pickle
from app import app, db, downloader, feature_extractor, inferencer
from config import config
from flask import request
from uuid import uuid4
import shutil

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
        return db.songs.find({})
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
            dto = request.get_json()
            
            # Download song
            print("Downloading song")
            downloader.download(tmp_path, dto['yt_link'])
            
            # Generate features
            print("Generating features")
            entries = os.listdir(tmp_path)
            for entry in entries:
                features = feature_extractor.extract(os.path.realpath(entry))
                title = entry.split('.')[0]
            hpcp_pickle = pymongo.binary.Binary( pickle.dumps(features[0], protocol=2) )
            mfcc_pickle = pymongo.binary.Binary( pickle.dumps(features[1], protocol=2) )
            
            # Generate embeddings
            print("Generating embeddings")
            emb = inferencer.generate_embeddings(features[0])
            emb_pickle = pymongo.binary.Binary( pickle.dumps(emb, protocol=2) )
        
            dto['title'] = title
            dto['upload_date'] = datetime.now()
            dto['features'] = {
                'hpcp': hpcp_pickle,
                'mfcc': mfcc_pickle
            }
            dto['version'] = config.APP_VERSION
            dto['embeddings'] = emb_pickle
            
            print("Saved to database")
            return db.songs.insert_one(dto), 200
        except Exception as e:
            return str(e), 500
        finally:
            shutil.rmtree(tmp_path)
        