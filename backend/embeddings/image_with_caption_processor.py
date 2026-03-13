#from embeddings.image_embeddings import get_clip_embedding
from backend.embeddings.text_embeddings import get_text_embedding
from backend.embeddings.multimodal_embeddings import get_image_embedding


# def process_image_with_caption(image_path, caption):

#     image_embedding = get_clip_embedding(image_path)

#     caption_embedding = get_text_embedding(caption)

#     return {
#         "image_embedding": image_embedding,
#         "caption_embedding": caption_embedding
#     } 


def process_image_with_caption(image_path, caption):

    image_embedding = get_image_embedding(image_path)

    caption_embedding = None

    if caption and len(caption.strip()) > 0:
        caption_embedding = get_text_embedding(caption)

    return {
        "image_embedding": image_embedding,
        "caption_embedding": caption_embedding
    }