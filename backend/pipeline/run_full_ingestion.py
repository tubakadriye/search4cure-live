from ingestion.arxiv_loader import ArxivPDFLoader
from ingestion.page_extractor import extract_pages
from ingestion.image_extractor import extract_images
from ingestion.table_extractor import extract_tables_from_pdf
from ingestion.entity_extractor import extract_entities_with_llm
from ingestion.caption_extractor import extract_captions

from embeddings.image_with_caption_processor import process_image_with_caption

from graph.node_builder import build_nodes, build_image_nodes, build_page_nodes, build_table_nodes
from graph.edge_builder import build_edges

from database.spanner_writer import insert_nodes, insert_edges
from database.spanner_client import get_database


def run_pipeline():

    print("Downloading papers from arXiv...")

    loader = ArxivPDFLoader(
        query="diabetes",
        max_docs=300
    )

    papers = loader.download_pdfs()

    database = get_database()

    for paper in papers:
        print("Processing:", paper["title"])

        pdf = paper["pdf"]

        # -------- PAGE EXTRACTION --------
        print("Extracting pages")
        pages = extract_pages(pdf,  paper["arxiv_id"])
        full_text = " ".join([p["text"] for p in pages])

        # -------- ENTITY EXTRACTION --------
        print("Extracting entities with LLM...")
        entities = extract_entities_with_llm(full_text)

        # -------- IMAGE EXTRACTION --------
        print("Extracting images...")
        images = extract_images(pdf)

        # -------- CAPTION EXTRACTION --------
        print("Extracting captions")
        page_caption_map = {}

        for page in pages:

            captions = extract_captions(page["text"])

            page_caption_map[page["page_number"]] = captions


        # -------- IMAGE + CAPTION EMBEDDINGS --------
        print("Image and caption embeddings...")

        for img in images:
            page_caps = page_caption_map.get(img["page_number"], [])

            caption = page_caps[0] if page_caps else ""

            embeddings = process_image_with_caption(img["path"], caption)

            img["caption"] = caption
            img["image_embedding"] = embeddings["image_embedding"]
            img["caption_embedding"] = embeddings["caption_embedding"]
        
        # -------- TABLE EXTRACTION --------
        print("Extracting tables...")
        tables = extract_tables_from_pdf(pdf)

        # -------- GRAPH BUILDING --------
        print("Building graph structure...")
        nodes = build_nodes(paper, entities, full_text)
        edges = build_edges(paper, pages, entities, images, tables)

        page_nodes = build_page_nodes(pages)
        image_nodes = build_image_nodes(paper["arxiv_id"], images)
        table_nodes = build_table_nodes(paper["arxiv_id"], tables)

        # -------- INSERT INTO SPANNER --------
        print("Inserting into Spanner...")
        insert_nodes(database, nodes)
        insert_nodes(database, page_nodes)
        insert_nodes(database, image_nodes)
        insert_nodes(database, table_nodes)
        

        insert_edges(database, edges)

        print("Processed:", paper["title"])


    print("Pipeline completed successfully!")



if __name__ == "__main__":
    run_pipeline()


#uv run python backend/pipeline/run_full_ingestion.py
