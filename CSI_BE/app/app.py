from pymongo import MongoClient
from config import config
from flask import Flask
from feature_extraction.downloader import YoutubeDownloader

from feature_extraction.extraction import FeatureExtractor
from model.inference import Inference

app = Flask(__name__)

db_client = MongoClient(config.MONGO_URL)
db = db_client.test

feature_extractor = FeatureExtractor(config.FEATURE)
downloader = YoutubeDownloader()

inferencer = Inference(config.SCALE, config.THRESHOLD_FULL, config.THRESHOLD_SEG, config.FRAME_SIZE)