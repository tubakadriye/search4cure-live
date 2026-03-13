from backend.utils.gcs_utils import upload_table_to_gcs
from backend.embeddings.table_embeddings import embed_table
#import json
from backend.embeddings.text_embeddings import get_text_embedding
from google.cloud import spanner


def build_nodes(paper, entities, full_text):

    nodes = []

    text_embedding = get_text_embedding(full_text)

    # -------------------------
    # Paper node
    # -------------------------

    nodes.append({
        "table": "Papers",
        "paper_id": paper["arxiv_id"],
        "title": paper["title"],
        "abstract": full_text[:2000],
        "text_embedding": text_embedding,
        "created_at": spanner.COMMIT_TIMESTAMP
    })

    # -------------------------
    # Authors
    # -------------------------

    for a in entities.get("authors", []):
        nodes.append({
            "table": "Authors",
            "author_id": a.lower().replace(" ", "_"),
            "name": a,
            "created_at": spanner.COMMIT_TIMESTAMP
        })


    # -------------------------
    # Methods
    # -------------------------

    for m in entities["methods"]:
        nodes.append({
            "table": "Methods",
            "method_id": m.lower().replace(" ", "_"),
            "name": m,
            "created_at": spanner.COMMIT_TIMESTAMP
        })

    # -------------------------
    # Diseases
    # -------------------------

    for d in entities["diseases"]:
        nodes.append({
            "table": "Diseases",
            "disease_id": d.lower().replace(" ", "_"),
            "name": d,
            "created_at": spanner.COMMIT_TIMESTAMP
        })

    # -------------------------
    # Datasets
    # -------------------------

    for ds in entities["datasets"]:
        nodes.append({
            "table": "Datasets",
            "dataset_id": ds.lower().replace(" ", "_"),
            "name": ds,
            "created_at": spanner.COMMIT_TIMESTAMP
        })

    
    # -------------------------
    # Biomarkers
    # -------------------------

    for b in entities.get("biomarkers", []):
        nodes.append({
            "table": "Biomarkers",
            "biomarker_id": b.lower().replace(" ", "_"),
            "name": b,
            "created_at": spanner.COMMIT_TIMESTAMP
        })

    # -------------------------
    # Drugs
    # -------------------------

    for drug in entities.get("drugs", []):
        nodes.append({
            "table": "Drugs",
            "drug_id": drug.lower().replace(" ", "_"),
            "name": drug,
            "created_at": spanner.COMMIT_TIMESTAMP
        })

    # -------------------------
    # Genes
    # -------------------------

    for g in entities.get("genes", []):
        nodes.append({
            "table": "Genes",
            "gene_id": g.lower().replace(" ", "_"),
            "name": g,
            "created_at": spanner.COMMIT_TIMESTAMP
        })


    # -------------------------
    # Outcomes
    # -------------------------

    for o in entities.get("outcomes", []):
        nodes.append({
            "table": "Outcomes",
            "outcome_id": o.lower().replace(" ", "_"),
            "name": o,
            "created_at": spanner.COMMIT_TIMESTAMP
        })


    return nodes

    


def build_table_nodes(paper_id, tables):
    nodes = []

    for t in tables:
        table_id = f"{paper_id}_p{t['page_number']}_t{t['table_index']}"

        gcs_key = upload_table_to_gcs(t["dataframe"])

        nodes.append({
            "table": "Tables",
            "table_id": table_id,
            "paper_id": paper_id,
            "page_number": t["page_number"],
            "table_json": gcs_key,
            "table_embedding": embed_table(t["dataframe"]),
            "created_at": spanner.COMMIT_TIMESTAMP
        })

    return nodes


def build_image_nodes(paper_id, images):

    nodes = []

    for img in images:

        nodes.append({
            "table": "Images",
            "image_id": img["image_id"],
            "paper_id": paper_id,
            "page_number": img["page_number"],
            "gcs_key": img["gcs_key"],
            "width": img["width"],
            "height": img["height"],
            "caption": img.get("caption"),
            "image_embedding": img.get("image_embedding"),
            "caption_embedding": img.get("caption_embedding"),
            "created_at": spanner.COMMIT_TIMESTAMP
        })

    return nodes


def build_page_nodes(pages):

    nodes = []

    for p in pages:
        nodes.append({
            "table": "Pages",
            "page_id": p["page_id"],
            "paper_id": p["paper_id"],
            "page_number": p["page_number"],
            "text": p["text"],
            "text_embedding": p["text_embedding"],
            "created_at": spanner.COMMIT_TIMESTAMP
        })

    return nodes

