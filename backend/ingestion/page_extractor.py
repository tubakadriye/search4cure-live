import fitz
from embeddings.text_embeddings import get_text_embedding

def extract_pages(pdf, paper_id):

    pages = []

    for i, page in enumerate(pdf):

        text = page.get_text()

        embedding = None
        if text.strip():
            embedding = get_text_embedding(text)

        pages.append({
            "page_id": f"{paper_id}_page_{i+1}",
            "paper_id": paper_id,
            "page_number": i+1,
            "text": text,
            "text_embedding": embedding
        })

    return pages
