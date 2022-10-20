from pymongo import MongoClient
from config import config
from flask import Flask
from feature_extraction.downloader import YoutubeDownloader

from feature_extraction.extraction import FeatureExtractor
from model.inference import Inference

app = Flask(__name__)

db_client = MongoClient(config.MONGO_URL)
db = db_client.test

feature_extractor = FeatureExtractor()
downloader = YoutubeDownloader()

inferencer = Inference()