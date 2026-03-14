from typing import List, Union
from PIL import Image
import vertexai
from vertexai.preview.vision_models import MultiModalEmbeddingModel
import tempfile
import os
from vertexai.vision_models import Image


# Initialize Vertex AI
PROJECT_ID = os.getenv("PROJECT_ID", "search4cure-diabetes")
REGION = os.getenv("REGION", "us-central1")

vertexai.init(project=PROJECT_ID, location=REGION)

# Initialize your GCS client and bucket
GCS_BUCKET = os.getenv("GCS_BUCKET", "diabetes-rag-assets")

# Load model
model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")

def get_image_embedding(gcs_key):

    gcs_uri = f"gs://{GCS_BUCKET}/{gcs_key}"

    image = Image.load_from_file(gcs_uri)

    embeddings = model.get_embeddings(
        image=image
    )

    return embeddings.image_embedding


# def get_multimodal_embedding(data: Union[Image.Image, str]) -> List[float]:
#     """
#     Generate embeddings for text or images using Vertex AI multimodal embeddings.

#     Args:
#         data (Image.Image | str): Image or text input.

#     Returns:
#         List[float]: embedding vector
#     """

#     try:

#         # TEXT EMBEDDING
#         if isinstance(data, str):

#             embeddings = model.get_embeddings(
#                 contextual_text=data
#             )

#             return embeddings.text_embedding


#         # IMAGE EMBEDDING
#         elif isinstance(data, Image.Image):

#             # Save image temporarily
#             with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:

#                 data.save(tmp.name)
#                 image_path = tmp.name

#             embeddings = model.get_embeddings(
#                 image=image_path
#             )

#             os.remove(image_path)

#             return embeddings.image_embedding


#         else:
#             raise ValueError("Input must be text or PIL Image.")

#     except Exception as e:

#         print(f"[!] Vertex embedding failed: {e}")
#         return []
    

# def get_image_embedding(image_path):

#     embeddings = model.get_embeddings(
#         image=image_path
#     )

#     return embeddings.image_embedding


