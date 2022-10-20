import os

class Config:
    APP_VERSION = "1.0"
    
    DATA_DIR = os.getenv("MONGO_URL", "/tmp")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    MONGO_URL = os.getenv("MONGO_URL", None)
    
config = Config()