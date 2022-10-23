from model.cnn import from_config
import torch
import numpy as np 
from torch.nn import functional as F

class Inference:
    def __init__(self, scale, threshold=0.13) -> None:
        self.model = from_config('/home/petros/cover-song-identification-platform/csi_be/resources/config.json')
        chk = torch.load('/home/petros/cover-song-identification-platform/csi_be/resources/checkpoint.tar', map_location=torch.device("cpu")) 
        self.model.load_state_dict(chk['model_state_dict'])
        print("loaded pretrained model")
        self.model.eval()
        
        self.D = threshold
        self.scale=scale
        
    def generate_embeddings(self, features):
        with torch.no_grad():
            repr = self.segment_and_scale(features)
            x = torch.tensor(repr)
            return self.model(x).squeeze(0).numpy()
    
    def predict(self, emb1, emb2):        
        dist = torch.norm(emb1 - emb2, dim=1)
        inv = 1/torch.sqrt(dist)
        return (inv > self.D)*1, dist
    
    def segment_and_scale(self, repr):
        """
        Take an np.array of shape num_features x num_samples, split into segments and scale to specific size
        in order to create CNN inputs.
        
        Returns: num_segs X num_channels X num_features X num_samples
        """
        if type(repr) in (torch.tensor, np.ndarray):
            repr = torch.tensor(repr)
            frames = repr.unsqueeze(0)
            frames = frames.unsqueeze(1)
            print(frames.size())
            frames = F.interpolate(frames, scale_factor=self.scale)
            return frames
        else:
            raise ValueError("unsupported repr type")