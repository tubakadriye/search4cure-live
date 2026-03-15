from google.cloud import spanner
from backend.utils.id_utils import generate_id


def build_edges(paper, pages, entities, images=None, tables=None):

    edges = []

    paper_id = paper["arxiv_id"]

    def add(table, key, values, prefix):
        for v in values:
            entity_id = generate_id(v, prefix)
            edges.append({
                "table": table,
                "paper_id": paper_id,
                key: entity_id,
                "created_at": spanner.COMMIT_TIMESTAMP
            })

    add("PaperUsesMethod", "method_id", entities.get("methods", []), prefix="method")
    add("PaperHasAuthor", "author_id", entities.get("authors", []), prefix="author")
    add("PaperStudiesDisease", "disease_id", entities.get("diseases", []), prefix="disease")
    add("PaperUsesDataset", "dataset_id", entities.get("datasets", []), prefix="dataset")
    add("PaperMentionsBiomarker", "biomarker_id", entities.get("biomarkers", []), prefix="biomarker")
    add("PaperMentionsGene", "gene_id", entities.get("genes", []), prefix="gene")
    add("PaperReportsOutcome", "outcome_id", entities.get("outcomes", []), prefix="outcome")

    # -----------------------------
    # Pages
    # -----------------------------

    for p in pages:
        edges.append({
            "table": "PaperHasPage",
            "paper_id": paper_id,
            "page_id": p["page_id"],
            "created_at": spanner.COMMIT_TIMESTAMP
        })


    # -----------------------------
    # Images
    # -----------------------------
    if images:
        for img in images:
            # Link image to paper
            edges.append({
                "table": "PaperHasImage",
                "paper_id": paper_id,
                "image_id": img["image_id"],
                "created_at": spanner.COMMIT_TIMESTAMP
            })
            # Link image to page

            edges.append({
                "table": "PageHasImage",
                "page_id": img["page_id"],
                "image_id": img["image_id"],
                "created_at": spanner.COMMIT_TIMESTAMP
            })

    # -----------------------------
    # Tables
    # -----------------------------
    if tables:
        for t in tables:
            table_id = generate_id(f"{paper_id}_p{t['page_number']}_t{t['table_index']}", "table")

            edges.append({
                "table": "PaperHasTable",
                "paper_id": paper_id,
                "table_id": table_id,
                "created_at": spanner.COMMIT_TIMESTAMP
            })

    return edges





    # # -----------------------------
    # # Methods
    # # -----------------------------

    # for method in entities.get("methods", []):
    #     edges.append({
    #         "table": "PaperUsesMethod",
    #         "paper_id": paper_id,
    #         "method_id": method.lower().replace(" ", "_")
    #     })


    # # -----------------------------
    # # Authors
    # # -----------------------------

    # for a in entities.get("authors", []):
    #     edges.append({
    #         "table": "PaperHasAuthor",
    #         "paper_id": paper_id,
    #         "author_id": a.lower().replace(" ", "_")
    #     })

    # # -----------------------------
    # # Diseases
    # # -----------------------------
    # for disease in entities.get("diseases", []):
    #     edges.append({
    #         "table": "PaperStudiesDisease",
    #         "paper_id": paper_id,
    #         "disease_id": disease.lower().replace(" ", "_")
    #     })

    # # -----------------------------
    # # Datasets
    # # -----------------------------
    # for dataset in entities.get("datasets", []):
    #     edges.append({
    #         "table": "PaperUsesDataset",
    #         "paper_id": paper_id,
    #         "dataset_id": dataset.lower().replace(" ", "_")
    #     })

    # # -----------------------------
    # # Biomarkers
    # # -----------------------------
    # for biomarker in entities.get("biomarkers", []):
    #     edges.append({
    #         "table": "PaperMentionsBiomarker",
    #         "paper_id": paper_id,
    #         "biomarker_id": biomarker.lower().replace(" ", "_")
    #     })

    
    # # -------------------------
    # # Genes
    # # -------------------------

    # for gene in entities.get("genes", []):
    #     edges.append({
    #         "table": "PaperMentionsGene",
    #         "paper_id": paper_id,
    #         "gene_id": gene.lower().replace(" ", "_")
    #     })

    # # -------------------------
    # # Outcomes
    # # -------------------------

    # for outcome in entities.get("outcomes", []):
    #     edges.append({
    #         "table": "PaperReportsOutcome",
    #         "paper_id": paper_id,
    #         "outcome_id": outcome.lower().replace(" ", "_")
    #     })




