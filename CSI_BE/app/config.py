import os

class Config:
    APP_VERSION = "1.993"
    
    DATA_DIR = os.getenv("DATA_DIR", "/tmp")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    MONGO_URL = os.getenv("MONGO_URL", None)
    print(MONGO_URL)
    
    FEATURE = "hpcp"
    SCALE = (1, 0.2)
    THRESHOLD_FULL =  1.15 #1.65
    THRESHOLD_SEG = 1.08 #1.57
    FRAME_SIZE = 3600
    
config = Config()