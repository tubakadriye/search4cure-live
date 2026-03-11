from vertexai.language_models import TextEmbeddingModel

model = TextEmbeddingModel.from_pretrained("text-embedding-004")

def get_text_embedding(text):

    embedding = model.get_embeddings([text])[0].values

    return embedding


