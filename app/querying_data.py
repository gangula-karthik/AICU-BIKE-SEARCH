import torch
import clip
from PIL import Image
from io import BytesIO
import numpy as np
import requests

def process_and_query_text(text, model, device, collection, n_results=6):
    model.eval()
    model.to(device)
    
    with torch.no_grad():
        text_input = clip.tokenize([text], truncate=True).to(device)
        text_feature = model.encode_text(text_input).float()
        text_feature /= text_feature.norm(dim=-1, keepdim=True)
        query_embeddings = text_feature.detach().cpu().numpy()
        
    results = collection.query(
        query_embeddings=query_embeddings,
        n_results=n_results
    )

    return results


def process_and_query_image_url(image_input, model, device, collection, n_results=6):
    model.eval()
    model.to(device)
    
    with torch.no_grad():
        image_feature = model.encode_image(image_input).float()
        image_feature /= image_feature.norm(dim=-1, keepdim=True)
        query_embeddings = image_feature.detach().cpu().numpy()
        
    results = collection.query(
        query_embeddings=query_embeddings,
        n_results=n_results
    )

    return results