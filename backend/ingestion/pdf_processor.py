# multimodal/pdf_processing.py
from tqdm import tqdm
from utils.gcs_utils import upload_image_to_gcs
from PIL import Image
from io import BytesIO

import fitz  # PyMuPDF

from embeddings.image_embeddings import get_clip_embedding

def process_pdfs_and_upload_images(all_pdfs, mat=None):
    docs = []
    if mat is None:
        mat = fitz.Matrix(2, 2)  # default zoom

    for pdf_idx, pdf_info in enumerate(all_pdfs):
        pdf = pdf_info["pdf"]
        title = pdf_info.get("title", f"pdf_{pdf_idx+1}")
        url = pdf_info.get("url", "N/A")

        safe_title = title.replace(" ", "_").replace("/", "_")

        for page_idx in tqdm(range(pdf.page_count), desc=f"PDF {pdf_idx + 1}"):
            temp = {}
            page = pdf[page_idx]
            
            #TEXT
            text = page.get_text()
            temp["page_text"] = text

            if text.strip():
                try:
                    temp["sbert_text_embedding"] = get_sbert_embedding(text)
                except Exception as e:
                    print(f"[!] SBERT embedding failed on page {page_idx+1}: {e}")
                try:
                    temp["clip_text_embedding"] = get_clip_embedding(text)
                except Exception as e:
                    print(f"[!] CLIP text embedding failed on page {page_idx+1}: {e}")

            # IMAGE
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")

            gcs_key = f"multimodal-rag/{safe_title}_page_{page_idx+1}.png"
            upload_image_to_gcs(gcs_key, img_bytes)

            try:
                img = Image.open(BytesIO(img_bytes))
                temp["clip_image_embedding"] = get_clip_embedding(img)
            except Exception as e:
                print(f"[!] CLIP image embedding failed on page {page_idx+1}: {e}")

            # Metadata
            temp["image"] = img_bytes
            temp["gcs_key"] = gcs_key
            temp["width"] = pix.width
            temp["height"] = pix.height
            temp["pdf_title"] = title
            temp["url"] = url
            temp["page_number"] = page_idx + 1
            docs.append(temp)

        pdf.close()

    return docs


def process_and_embed_docs(pdfs=None, uploaded_image=None, image_name=None, get_embedding=None):
    from .pdf_processor import process_pdfs_and_upload_images  # avoid circular import

    docs = []

    # --- Process PDFs ---
    if pdfs:
        pdf_docs = process_pdfs_and_upload_images(pdfs)
        docs.extend(pdf_docs)

    # --- Process Uploaded Image ---
    if uploaded_image and image_name:
        image = Image.open(uploaded_image).convert("RGB")
        image_bytes_io = BytesIO()
        image.save(image_bytes_io, format="PNG")
        img_bytes = image_bytes_io.getvalue()

        safe_name = image_name.strip().replace(" ", "_").replace("/", "_")
        gcs_key = f"multimodal-rag/{safe_name}.png"
        upload_image_to_gcs(gcs_key, img_bytes)

        try:
            clip_emb = get_embedding(image)
        except Exception as e:
            print(f"[!] CLIP embedding failed for uploaded image: {e}")
            clip_emb = None

        image_doc = {
            "clip_embedding": clip_emb,
            "image": img_bytes,
            "gcs_key": gcs_key,
            "width": image.width,
            "height": image.height,
            "pdf_title": image_name.strip(),
            "url": "User Uploaded Image",
            "page_number": 1
        }
        docs.append(image_doc)

    return docs
