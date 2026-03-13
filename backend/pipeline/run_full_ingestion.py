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
from tqdm import tqdm


def run_pipeline():
    print("Initializing Arxiv PDF loader...")

    loader = ArxivPDFLoader(
        query="diabetes",
        max_docs=300,
        delay=2
    )

    #papers = loader.download_pdfs()

    database = get_database()

    total_nodes, total_edges = [], []

    print("Streaming papers from arXiv...")
    for paper in tqdm(loader.stream_pdfs(), desc="Papers", unit="paper"):
        pdf = paper["pdf"]
        paper_id = paper["arxiv_id"]
        print(f"\nProcessing paper: {paper['title']} ({paper_id})")

        # -------- PAGE EXTRACTION --------
        print("Extracting pages...")
        pages = extract_pages(pdf,  paper_id)
        full_text = " ".join([p["text"] for p in pages])

        # -------- ENTITY EXTRACTION --------
        print("Extracting entities")
        entities = extract_entities_with_llm(full_text)

        # -------- IMAGE EXTRACTION --------
        print("Extracting images...")
        images = extract_images(pdf, paper_id)

        # -------- CAPTION EXTRACTION --------
        print("Extracting captions per page...")
        page_caption_map = {}
        for page in pages:
            captions = extract_captions(page["text"])
            page_caption_map[page["page_number"]] = captions

        # -------- IMAGE + CAPTION EMBEDDINGS --------
        print("Processing image + caption embeddings...")
        for img in images:
            captions = page_caption_map.get(img["page_number"], [])
            caption = captions[0] if captions else ""
            embeddings = process_image_with_caption(img["gcs_key"], caption)
            img["caption"] = caption
            img["image_embedding"] = embeddings["image_embedding"]
            img["caption_embedding"] = embeddings["caption_embedding"]
        
        # -------- TABLE EXTRACTION --------
        print("Extracting tables...")
        tables = extract_tables_from_pdf(pdf)

        # -------- GRAPH BUILDING --------
        print("Building graph structure...")

        page_nodes = build_page_nodes(pages)
        image_nodes = build_image_nodes(paper_id, images)
        table_nodes = build_table_nodes(paper_id, tables)

        nodes = build_nodes(paper, entities, full_text)
        edges = build_edges(paper, pages, entities, images, tables)

        # -------- INSERT INTO SPANNER --------
        print("Inserting nodes and edges into Spanner...")
        insert_nodes(database, nodes + page_nodes + image_nodes + table_nodes)
        insert_edges(database, edges)

        total_nodes.extend(nodes + page_nodes + image_nodes + table_nodes)
        total_edges.extend(edges)

        # all_nodes.extend(nodes)
        # all_nodes.extend(page_nodes)
        # all_nodes.extend(image_nodes)
        # all_nodes.extend(table_nodes)

        # all_edges.extend(edges)

        print(f"Completed paper: {paper['title']} ({paper_id})")

        # insert_nodes(database, nodes)
        # insert_nodes(database, page_nodes)
        # insert_nodes(database, image_nodes)
        # insert_nodes(database, table_nodes)
        

        #insert_edges(database, edges)

    
    #print("Writing batched data to Spanner...")

    # insert_nodes(database, all_nodes)
    # insert_edges(database, all_edges)

    print("\nPipeline completed successfully!")
    print(f"Total nodes inserted: {len(total_nodes)}")
    print(f"Total edges inserted: {len(total_edges)}")



if __name__ == "__main__":
    run_pipeline()


#uv run python backend/pipeline/run_full_ingestion.py
