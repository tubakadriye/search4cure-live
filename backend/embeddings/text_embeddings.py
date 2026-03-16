from vertexai.language_models import TextEmbeddingModel
import vertexai
import os

vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
)

model = TextEmbeddingModel.from_pretrained("textembedding-gecko-004")

def get_text_embedding(text):

    embedding = model.get_embeddings([text])[0].values

    return embedding


