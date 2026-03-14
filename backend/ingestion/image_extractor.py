import fitz
import io
import os
import uuid
from PIL import Image
from backend.utils.gcs_utils import upload_bytes_to_gcs
from backend.embeddings.image_with_caption_processor import process_image_with_caption


def extract_images(pdf, paper_id):
    os.makedirs("data/images", exist_ok=True)

    images = []   

    for page_index in range(len(pdf)):

        page = pdf[page_index]
        
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):

            xref = img[0]

            base = pdf.extract_image(xref)

            image_bytes = base["image"]

            #image = Image.open(io.BytesIO(image_bytes))

            image_id = f"page{page_index+1}_img{img_index}"

            gcs_key = upload_bytes_to_gcs(image_bytes, "images", "image/png")
  

            path = f"data/images/{image_id}.png"

            with open(path, "wb") as f:
                f.write(image_bytes)

            images.append({
                "image_id": image_id,
                "paper_id": paper_id,
                "page_number": page_index + 1,
                "page_id": f"{paper_id}_page_{page_index+1}",
                "path": path,
                "gcs_key": gcs_key,
                "width": base["width"],
                "height": base["height"]
            })

    return images
