from model.cnn import from_config
import torch
import numpy as np 
from torch.nn import functional as F

class Inference:
    def __init__(self, scale, threshold, frame_size) -> None:
        self.model = from_config('/home/petros/cover-song-identification-platform/CSI_BE/app/resources/config.json')
        chk = torch.load('/home/petros/cover-song-identification-platform/CSI_BE/app/resources/checkpoint.tar', map_location=torch.device("cpu")) 
        self.model.load_state_dict(chk['model_state_dict'])
        print("loaded pretrained model")
        self.model.eval()
        
        self.D = threshold
        self.scale=scale
        self.frame_size=frame_size
        
    def generate_embeddings(self, features, segment=True):
        with torch.no_grad():
            repr = self.segment_and_scale(features, segment)
            x = torch.tensor(repr)
            return self.model(x)
    
    def predict(self, emb1, emb2):        
        dist = torch.norm(emb1 - emb2, dim=1)
        inv = 2 - dist
        mean_inv = np.mean(inv.tolist())
        return (inv > self.D)*1, dist, bool(mean_inv > self.D)
    
    def generate_segments(self, song: np.array, step=400, overlap=0.5):
        """
        Segment a #num_features X num_samples vector into windows.

        Arguments:
            song: np.array or array like of shape num_features x num_samples
            step: the window_size
            overlap: the overlap percentage between windows

        To calculate the time is seconds for each window use the following formula:
        T = step * hop_size / sample_freq
        In the case of mfcc for example, T = step * 512 / 22050

        Returns a python list of shape num_segments X num_features X num_samples
        """
        return [
            song[..., i : step + i]
            for i in np.arange(0, song.shape[-1] - step, int(step * overlap))
        ]
    
    def segment_and_scale(self, repr, segment=True):
        """
        Take an np.array of shape num_features x num_samples, split into segments and scale to specific size
        in order to create CNN inputs.
        
        Returns: num_segs X num_channels X num_features X num_samples
        """
        if type(repr) in (torch.tensor, np.ndarray):
            repr = torch.tensor(repr)
            if segment:
                repr = torch.stack(self.generate_segments(repr, step=self.frame_size))
            else:
                repr = repr.unsqueeze(0)
            frames = repr.unsqueeze(1)
            frames = F.interpolate(frames, scale_factor=self.scale)
            return frames
        else:
            raise ValueError("unsupported repr type")