import os

class Config:
    APP_VERSION = "1.0"
    
    DATA_DIR = os.getenv("DATA_DIR", "/tmp")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    MONGO_URL = os.getenv("MONGO_URL", None)
    
    FEATURE = "hpcp"
    SCALE = (1, 0.2)
    
config = Config()