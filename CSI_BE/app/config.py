import os

class Config:
    APP_VERSION = "1.7"
    
    DATA_DIR = os.getenv("DATA_DIR", "/tmp")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    MONGO_URL = os.getenv("MONGO_URL", None)
    print(MONGO_URL)
    
    FEATURE = "hpcp"
    SCALE = (1, 0.2)
    THRESHOLD = 1.646 #1.26
    FRAME_SIZE = 3600 #1600
    
config = Config()