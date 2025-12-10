import torch
import clip
from PIL import Image

class CLIPLoader:
    def __init__(self, model_name="ViT-B/32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(model_name, self.device)

    def embed_text(self, text: str):
        tokens = clip.tokenize([text]).to(self.device)
        with torch.no_grad():
            return self.model.encode_text(tokens).cpu().numpy()[0]

    def embed_image(self, image_path: str):
        image = Image.open(image_path).convert("RGB")
        img_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            return self.model.encode_image(img_tensor).cpu().numpy()[0]
