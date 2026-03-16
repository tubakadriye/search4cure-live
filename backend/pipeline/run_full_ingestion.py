import os
import logging
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# -------------------- SETTINGS --------------------
os.environ["GOOGLE_CLOUD_DISABLE_METRICS"] = "true"
os.environ["OTEL_METRICS_EXPORTER"] = "none"
os.environ["OTEL_TRACES_EXPORTER"] = "none"
os.environ["SPANNER_ENABLE_METRICS"] = "false"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

from backend.ingestion.arxiv_loader import ArxivPDFLoader
from backend.ingestion.page_extractor import extract_pages
from backend.ingestion.image_extractor import extract_images
from backend.ingestion.table_extractor import extract_tables_from_pdf
from backend.ingestion.entity_extractor import extract_entities_with_llm
from backend.ingestion.caption_extractor import extract_captions
from backend.embeddings.image_with_caption_processor import process_image_with_caption
from backend.graph.node_builder import build_nodes, build_image_nodes, build_page_nodes, build_table_nodes
from backend.graph.edge_builder import build_edges
from backend.database.spanner_writer import insert_nodes, insert_edges
from backend.database.spanner_client import get_database
from backend.utils.spanner_utils import get_existing_papers, paper_exists
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="vertexai")

BATCH_SIZE = 200  # nodes/edges per batch insert

# -------------------- PAPER PROCESSING --------------------
def process_paper(paper, database, max_pages_for_entities):
    paper_id = paper["arxiv_id"]
    logging.info(f"[{paper_id}] Processing paper: {paper['title']}")

    pdf = paper["pdf"]
    pages = extract_pages(pdf, paper_id)
    full_text = " ".join([p["text"] for p in pages])

    # -------- ENTITY EXTRACTION --------
    entities_all = {k: [] for k in ["authors","methods","diseases","datasets","biomarkers","drugs","genes","outcomes"]}


    for page in pages[:max_pages_for_entities]:
        retries = 0
        while retries < 5:
            try:
                page_entities = extract_entities_with_llm(page["text"]) or {}
                logging.info(f"[{paper_id}] Extracted entities page {page['page_number']}")
                time.sleep(1)  # prevent rate limits
                break

            except Exception as e:
                if "429" in str(e):
                    wait = 2 ** retries
                    logging.warning(f"[{paper_id}] Rate limit hit. Waiting {wait}s...")
                    time.sleep(wait)
                    retries += 1
                else:
                    logging.error(f"[{paper_id}] Entity extraction failed: {e}")
                    page_entities = {}
                    break

        for key in entities_all:
            entities_all[key].extend(page_entities.get(key, []))
            entities_all[key] = list(set(entities_all[key]))

    # -------- IMAGE & CAPTION EXTRACTION --------
    images = extract_images(pdf, paper_id)

    page_caption_map = {}
    for page in pages:
        page_caption_map[page["page_number"]] = extract_captions(page["text"])

    for img in images:
        captions = page_caption_map.get(img["page_number"], [])
        caption = captions[0] if captions else ""

        try:
            embeddings = process_image_with_caption(img["gcs_key"], caption)
            img["caption"] = caption
            img["image_embedding"] = embeddings["image_embedding"]
            img["caption_embedding"] = embeddings["caption_embedding"]
            logging.info(f"[{paper_id}] Processed image on page {img['page_number']}")
        except Exception as e:
            logging.warning(f"[{paper_id}] Image embedding failed: {e}")

    # -------- TABLE EXTRACTION --------
    tables = extract_tables_from_pdf(pdf)
    logging.info(f"[{paper_id}] Extracted {len(tables)} tables")

    # -------- GRAPH BUILDING --------
    page_nodes = build_page_nodes(pages)
    image_nodes = build_image_nodes(paper_id, images)
    table_nodes = build_table_nodes(paper_id, tables)

    nodes = build_nodes(paper, entities_all, full_text)
    edges = build_edges(paper, pages, entities_all, images, tables)

    return nodes + page_nodes + image_nodes + table_nodes, edges


# -------------------- PIPELINE --------------------
def run_pipeline(max_papers=300, max_pages_for_entities=3):
    logging.info("Initializing Arxiv PDF loader...")

    loader = ArxivPDFLoader(
        query="diabetes",
        max_docs=max_papers #300
    )

    #papers = loader.download_pdfs()

    database = get_database()

    total_nodes, total_edges = [], []
    batch_nodes, batch_edges = [], []

    existing_papers = get_existing_papers(database)
    logging.info("Streaming papers from arXiv...")

    papers = [
        p for p in loader.stream_pdfs()
        if p["arxiv_id"] not in existing_papers
    ]

    logging.info(f"{len(papers)} new papers to process")

    MAX_WORKERS = 4  # safe for Vertex AI
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(process_paper, paper, database, max_pages_for_entities)
            for paper in papers
        ]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing papers", file=sys.stdout):
            paper = futures[future]
            paper_id = paper["arxiv_id"]
            try:
                nodes, edges = future.result()
                batch_nodes.extend(nodes)
                batch_edges.extend(edges)
                total_nodes.extend(nodes)
                total_edges.extend(edges)

                if len(batch_nodes) > BATCH_SIZE:
                    insert_nodes(database, batch_nodes)
                    insert_edges(database, batch_edges)
                    batch_nodes, batch_edges = [], []
                    logging.info(f"[{paper_id}] Batch inserted {BATCH_SIZE} nodes/edges")

            except Exception as e:
                logging.error(f"[{paper_id}] Paper processing failed: {e}")

    # flush remaining batches
    if batch_nodes:
        try:
            insert_nodes(database, batch_nodes)
            insert_edges(database, batch_edges)
            logging.info(f"Final batch inserted {len(batch_nodes)} nodes/edges")
        except Exception as e:
            logging.error(f"Final batch insert failed: {e}")

    logging.info("\nPipeline completed successfully!")
    logging.info(f"Total nodes inserted: {len(total_nodes)}")
    logging.info(f"Total edges inserted: {len(total_edges)}")


#     print(f"Streaming up to {max_papers} papers from arXiv...")
#     for paper in tqdm(loader.stream_pdfs(), desc="Papers", unit="paper"):
#         pdf = paper["pdf"]
#         paper_id = paper["arxiv_id"]   

#         if paper_id in existing_papers:
#             continue

#         # if paper_exists(database, paper_id):
#         #     print(f"Skipping existing paper {paper_id}")
#         #     continue

#         print(f"\nProcessing paper: {paper['title']} ({paper_id})")

#         # -------- PAGE EXTRACTION --------
#         print("Extracting pages...")
#         pages = extract_pages(pdf,  paper_id)
#         full_text = " ".join([p["text"] for p in pages])

#         # -------- ENTITY EXTRACTION --------
#         print(f"Extracting entities from first {max_pages_for_entities} pages...")

#         entities_all = {
#             "authors": [],
#             "methods": [],
#             "diseases": [],
#             "datasets": [],
#             "biomarkers": [],
#             "drugs": [],
#             "genes": [],
#             "outcomes": []
#         }


#         for page in pages[:max_pages_for_entities]:
#             page_entities = {}
#             retries = 0

#             while retries < 5:
#                 try:
#                     page_entities = extract_entities_with_llm(page["text"]) or {}
#                     time.sleep(1)
#                     break
                
#                 except Exception as e:
#                     if "429" in str(e):
#                         wait = 2 ** retries
#                         print(f"Rate limit hit. Waiting {wait}s...")
#                         time.sleep(wait)
#                         retries += 1
#                     else:
#                         print(f"[Error] Entity extraction failed: {e}")
#                         page_entities = {}
#                         break
#             # Merge extracted entities
#             for key in entities_all.keys():
#                 entities_all[key].extend(page_entities.get(key, []))
#                 entities_all[key] = list(set(entities_all[key]))
#             if not page_entities:
#                 print(f"[Warning] No entities extracted from page {page['page_number']} of paper {paper_id}")


#         # -------- IMAGE EXTRACTION --------
#         print("Extracting images...")
#         images = extract_images(pdf, paper_id)
#         if not images:
#             print(f"[Warning] No images found in paper {paper_id}")

#         # -------- CAPTION EXTRACTION --------
#         print("Extracting captions per page...")
#         page_caption_map = {}
#         for page in pages:
#             captions = extract_captions(page["text"])
#             page_caption_map[page["page_number"]] = captions

#         # -------- IMAGE + CAPTION EMBEDDINGS --------
#         print("Processing image + caption embeddings...")
#         for img in images:
#             captions = page_caption_map.get(img["page_number"], [])
#             caption = captions[0] if captions else ""
#             try:
#                 embeddings = process_image_with_caption(img["gcs_key"], caption)
#                 img["caption"] = caption
#                 img["image_embedding"] = embeddings["image_embedding"]
#                 img["caption_embedding"] = embeddings["caption_embedding"]
#             except Exception as e:
#                 print(f"[Warning] Embedding failed for image on page {img['page_number']}: {e}")
        
#         # -------- TABLE EXTRACTION --------
#         print("Extracting tables...")
#         tables = extract_tables_from_pdf(pdf)
#         if not tables:
#             print(f"[Warning] No tables found in paper {paper_id}")

#         # -------- GRAPH BUILDING --------
#         print("Building graph structure...")

#         page_nodes = build_page_nodes(pages)
#         image_nodes = build_image_nodes(paper_id, images)
#         table_nodes = build_table_nodes(paper_id, tables)

#         nodes = build_nodes(paper, entities_all, full_text)
#         edges = build_edges(paper, pages, entities_all, images, tables)

#         # -------- BATCH INSERT INTO SPANNER --------
#         batch_nodes.extend(nodes + page_nodes + image_nodes + table_nodes)
#         batch_edges.extend(edges)

#         # flush batch if too big
#         if len(batch_nodes) > BATCH_SIZE:
#             try:
#                 insert_nodes(database, batch_nodes)
#                 insert_edges(database, batch_edges)
#             except Exception as e:
#                 print(f"[Error] Batch insert failed: {e}")
#             batch_nodes, batch_edges = [], []

#         # # -------- INSERT INTO SPANNER --------
#         # print("Inserting nodes and edges into Spanner...")
#         # insert_nodes(database, nodes + page_nodes + image_nodes + table_nodes)
#         # insert_edges(database, edges)

#         # -------- AGGREGATE TOTALS & LOG --------
#         total_nodes.extend(nodes + page_nodes + image_nodes + table_nodes)
#         total_edges.extend(edges)

#         print(f"Paper {paper_id} summary:")
#         print(f"  Nodes: {len(nodes) + len(page_nodes) + len(image_nodes) + len(table_nodes)}")
#         print(f"  Edges: {len(edges)}")
#         print(f"  Images: {len(images)} | Tables: {len(tables)}")
#         print(f"Completed paper: {paper['title']} ({paper_id})\n")
#         sys.stdout.flush()

#         # insert_nodes(database, nodes)
#         # insert_nodes(database, page_nodes)
#         # insert_nodes(database, image_nodes)
#         # insert_nodes(database, table_nodes)
        

#         #insert_edges(database, edges)

    
#     #print("Writing batched data to Spanner...")

#     # insert_nodes(database, all_nodes)
#     # insert_edges(database, all_edges)

#     # flush remaining nodes/edges
#     if batch_nodes:
#         try:
#             insert_nodes(database, batch_nodes)
#             insert_edges(database, batch_edges)
#         except Exception as e:
#             print(f"[Error] Final batch insert failed: {e}")

#     print("\nPipeline completed successfully!")
#     print(f"Total nodes inserted: {len(total_nodes)}")
#     print(f"Total edges inserted: {len(total_edges)}")



if __name__ == "__main__":
    # STEP 1: Run on 10 papers first
    #run_pipeline(max_papers=10, max_pages_for_entities=3)

    # STEP 2: Check your graph in Spanner
    # STEP 3: Scale to 100 papers
    # run_pipeline(max_papers=100, max_pages_for_entities=3)
    # STEP 4: Scale to 300 papers
    run_pipeline(max_papers=300, max_pages_for_entities=3)


#uv run python backend/pipeline/run_full_ingestion.py
