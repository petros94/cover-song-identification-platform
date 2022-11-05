from app import app, inferencer
from flask import request
import pandas as pd
import os
import logging
from datetime import datetime
import os
import pymongo
import pickle
from app import app, db, downloader, feature_extractor, inferencer
from endpoints.converters import convert_song_doc_to_dto
from config import config
from flask import request
from storage import upload_blob, download_blob
from uuid import uuid4
import shutil
import bson

# Get logger
logger = logging.getLogger(__name__)
# Create a handler
c_handler = logging.StreamHandler()
# link handler to logger
logger.addHandler(c_handler)
# Set logging level to the logger
logger.setLevel(logging.DEBUG) # <-- THIS!

@app.route("/tuning/threshold", methods=['PUT'])
def update_threshold():
    logger.info("Entered update_threshold")
    thr = request.get_json()['thr']
    inferencer.D = thr
    return {'result': 'OK'}, 200

@app.route("/tuning/loadsongs", methods=['POST'])
def load_songs():
    csv_path = '/home/petros/cover-song-identification-platform/CSI_BE/app/resources/songs.csv'
    links = pd.read_csv(csv_path)
    links.iterrows()
    for index, row in links.iterrows():
        for item in row[1:]:
            try:
                process(item)
            except Exception as e:
                print(e)
    return {'status': 'OK'}, 200
            
def process(link):
    request_id = str(uuid4())
    tmp_path = config.DATA_DIR + "/" + request_id
    os.makedirs(tmp_path)
    logger.info(f"tmp path: {tmp_path}")    
    res = db.songs.find_one({'yt_link': link})
    if res is not None:
        return convert_song_doc_to_dto(res), 200
    
    # Download song
    print("Downloading song")
    downloader.download(tmp_path, link)
    
    # Generate features
    print("Generating features")
    entry = os.listdir(tmp_path)[0]
    features = feature_extractor.extract(os.path.join(tmp_path, entry))
    title = entry.split('.')[0]
    hpcp_pickle = bson.binary.Binary( pickle.dumps(features, protocol=2) )
    
    # Generate embeddings
    print("Generating embeddings")
    emb = inferencer.generate_embeddings(features, segment=False)
    emb_seg = inferencer.generate_embeddings(features, segment=True)
    emb_pickle = bson.binary.Binary( pickle.dumps(emb.numpy(), protocol=2) )
    emb_seg_pickle = bson.binary.Binary( pickle.dumps(emb_seg.numpy(), protocol=2) )

    doc = {}
    doc['title'] = title
    doc['upload_date'] = datetime.now()
    doc['version'] = config.APP_VERSION
    doc['embeddings'] = emb_pickle
    doc['embeddings_seg'] = emb_seg_pickle
    doc['yt_link'] = link
    
    print("Saved to database")
    db.songs.insert_one(doc)
    
    doc = db.songs.find_one({'yt_link': link})
    
    upload_blob(str(doc['_id']), hpcp_pickle)