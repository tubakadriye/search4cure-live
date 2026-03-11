from typing import List

from PIL import Image
from sentence_transformers import SentenceTransformer

# Instantiate the CLIP model
clip_model = SentenceTransformer("clip-ViT-B-32")

def get_clip_embedding(data: Image.Image | str) -> List:
    """
    Get CLIP embeddings for images and text.

    Args:
        data (Image.Image | str): An image or text to embed.

    Returns:
        List: Embeddings as a list.
    """
    embedding = clip_model.encode(data).tolist()
    return embedding