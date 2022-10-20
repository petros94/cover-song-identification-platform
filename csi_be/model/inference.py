from cnn import from_config
import torch

class Inference:
    def __init__(self, threshold=0.13) -> None:
        self.model = from_config('resources/config.json')
        chk = torch.load('resources/checkpoint.tar', map_location=torch.device("cpu")) 
        self.model.load_state_dict(chk['model_state_dict'])
        print("loaded pretrained model")
        
        self.D = threshold
        
    def generate_embeddings(self, features):
        x = torch.tensor(features).unsqueeze(0)
        return self.model(x).squeeze(0).numpy()
    
    def predict(self, emb1, emb2):
        emb1 = emb1.unsqueeze()
        emb2 = emb2.unsqueeze()
        
        dist = torch.norm(emb1 - emb2, dim=1)
        inv = 1/torch.sqrt(dist)
        return (inv > self.D)*1, dist