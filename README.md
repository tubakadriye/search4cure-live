# search4cure-live

# Search4Cure

Search4Cure is a multimodal biomedical research assistant that builds a knowledge graph from research papers.

The system ingests research papers from arXiv, extracts structured information, generates embeddings, and stores everything in Google Cloud Spanner Property Graph.

It enables:

-  Semantic search

-  Entity-based search

- Image retrieval

- Table retrieval

- Knowledge graph exploration

---

## Architecture Diagram
```mermaid
flowchart TD

A[arXiv Papers] --> B[Download PDFs]

B --> C[PDF Processing]

C --> D1[Page Extraction]
C --> D2[Image Extraction]
C --> D3[Table Extraction]
C --> D4[Entity Extraction - Gemini]

D1 --> E[Generate Text Embeddings]
D2 --> F[Generate Image Embeddings]
D3 --> G[Generate Table Embeddings]

E --> H[Cloud Spanner Property Graph]
F --> H
G --> H
D4 --> H

H --> I[Hybrid Retrieval Engine]

I --> J1[Vector Search]
I --> J2[Graph Traversal]
I --> J3[Multimodal Search]

J1 --> K[Research Assistant]
J2 --> K
J3 --> K
```

## Data Processing Pipeline

![Data Processing Pipeline](./docs/Data%20Processing%20Pipeline.png)


mermaid
flowchart TD

A[arXiv] B[download_pdfs()]
B --> C[extract_pages()]
C --> D[extract_images()]
C --> E[extract_tables()]

C --> F[generate_text_embeddings()]
D --> G[generate_image_embeddings()]
E --> H[generate_table_embeddings()]

C --> I[extract_entities_with_llm()]

F --> J[build_graph_nodes_edges()]
G --> J
H --> J
I --> J

J --> K[insert_into_spanner()]


arXiv ingestion
        │
PDF parsing
        │
Entities (Gemini)
        │
Multimodal embeddings (Vertex AI)
        │
Graph + vectors
        │
Spanner
        │
Multimodal RAG
 

## Knowledge Graph Schema

```mermaid
graph TD

Paper -->|USES_METHOD| Method
Paper -->|USES_DATASET| Dataset
Paper -->|STUDIES_DISEASE| Disease
Paper -->|MENTIONS_BIOMARKER| Biomarker
Paper -->|HAS_IMAGE| Image
Paper -->|HAS_TABLE| Table
Paper -->|HAS_AUTHOR| Author

Drug -->|TREATS| Disease
Author -->|WROTE| Paper
Paper -->|CITES| Paper
```

## Multimodal Document Structure

```mermaid
graph TD

Paper --> Page

Page --> TextChunk
Page --> Image
Page --> Table

Image --> ImageEmbedding
TextChunk --> TextEmbedding
Table --> TableEmbedding
```

## Retrieval Architecture

```mermaid
flowchart TD

UserQuery --> Q1[Semantic Search]
UserQuery --> Q2[Image Search]
UserQuery --> Q3[Entity Query]

Q1 --> V[Vector Search - Text Embeddings]
Q2 --> I[Vector Search - Image Embeddings]
Q3 --> G[Graph Traversal]

V --> R[Results]
I --> R
G --> R

R --> AI[AI Research Assistant]
```

## System Deployment Architecture

```mermaid
flowchart TD

User --> UI[Streamlit / Frontend]

UI --> API[Cloud Run API]

API --> Agent[Agent Orchestrator]

Agent --> Spanner[(Cloud Spanner Graph)]
Agent --> VertexAI[Vertex AI - Gemini]

Spanner --> Embeddings[Vector Embeddings]
Spanner --> Graph[Knowledge Graph]

VertexAI --> Response

Embeddings --> Response
Graph --> Response

Response --> User
```

## Research Query Reasoning

```mermaid
graph TD

UserQuestion --> Paper

Paper --> Method
Paper --> Dataset
Paper --> Disease

Disease --> Biomarker
Drug --> Disease

Method --> Prediction
```

| Component       | Purpose                    |
| --------------- | -------------------------- |
| arXiv ingestion | Collect research papers    |
| PDF processing  | Extract multimodal content |
| Embeddings      | Enable semantic search     |
| Spanner Graph   | Store relationships        |
| Vector Search   | Retrieve relevant content  |
| Graph Traversal | Multi-hop reasoning        |

Example query reasoning:

Which papers predict diabetes progression?

Paper
 → Method (LSTM)
 → Dataset (UK Biobank)
 → Disease (Type 2 Diabetes)


# System Architecture

arXiv Papers
     │
     ▼
PDF Processing
 ├─ Page extraction
 ├─ Image extraction
 ├─ Table extraction
 └─ Entity extraction (Gemini)
     │
     ▼
Embedding Generation
 ├─ Text embeddings
 ├─ Image embeddings (CLIP / multimodal)
 └─ Caption embeddings
     │
     ▼
Cloud Spanner Property Graph
 ├─ Papers
 ├─ Pages
 ├─ Images
 ├─ Tables
 └─ Entities
     │
     ▼
Hybrid Retrieval
 ├─ Vector search
 ├─ Graph traversal
 └─ Multimodal search

## Knowledge Graph Structure

The system builds a biomedical research knowledge graph.

Paper
 ├── USES_METHOD → Method
 ├── USES_DATASET → Dataset
 ├── STUDIES_DISEASE → Disease
 ├── MENTIONS_BIOMARKER → Biomarker
 ├── HAS_IMAGE → Image
 ├── HAS_TABLE → Table
 └── HAS_AUTHOR → Author

### Multimodal Hierarchy

Paper
 ├── Page (text + embedding)
 │      ├── Images (image embeddings)
 │      └── Tables (table embeddings)
 │
 ├── Methods
 ├── Diseases
 ├── Datasets
 ├── Biomarkers
 └── Drugs

## Retrieval Capabilities

| Query Type     | Retrieval Method   |
| -------------- | ------------------ |
| Semantic text  | Page embeddings    |
| Image search   | Image embeddings   |
| Caption search | Caption embeddings |
| Table search   | Table embeddings   |
| Entity query   | Graph traversal    |


## Repository Structure

search4cure/
│
├── backend/
│   │
│   ├── ingestion/
│   │   ├── arxiv_loader.py
│   │   ├── pdf_processor.py
│   │   ├── page_extractor.py
│   │   └── entity_extractor.py
│   │
│   ├── embeddings/
│   │   ├── text_embeddings.py
│   │   ├── image_embeddings.py
│   │   └── multimodal_processor.py
│   │
│   ├── graph/
│   │   ├── graph_builder.py
│   │   ├── node_builder.py
│   │   └── edge_builder.py
│   │
│   ├── database/
│   │   ├── spanner_client.py
│   │   ├── spanner_writer.py
│   │   └── schema.sql
│   │
│   ├── retrieval/
│   │   ├── vector_search.py
│   │   ├── graph_queries.py
│   │   └── hybrid_retriever.py
│   │
│   ├── pipeline/
│   │   ├── build_graph_from_arxiv.py
│   │   ├── process_pdfs_pipeline.py
│   │   └── run_full_ingestion.py
│   │
│   └── api/
│       └── rag_api.py
│
├── scripts/
│   ├── setup_spanner_db.py
│   ├── setup_data.py
│   └── download_arxiv_papers.py
│
├── notebooks/
│   ├── test_arxiv_loader.ipynb
│   ├── test_embeddings.ipynb
│   └── test_entity_extraction.ipynb
│
├── data/
│   ├── pdfs/
│   ├── images/
│   └── metadata/
│
├── tests/
│   ├── test_graph_builder.py
│   ├── test_embeddings.py
│   └── test_arxiv_loader.py
│
├── requirements.txt
├── pyproject.toml
└── README.md


# Installation

## Install dependencies


pip install -r requirements.txt


or


uv sync


---

# Environment variables

Create `.env`


PROJECT_ID=search4cure-diabetes
INSTANCE_ID=diabetes-research-network
DATABASE_ID=research-graph-db
GRAPH_NAME=DiabetesResearchGraph
REGION=us-central1

## Google Cloud Setup

See [docs/cloud_setup.md](docs/cloud_setup.md) for full instructions on enabling required services and preparing the Google Cloud project.


---

# Create Spanner database


# Run ingestion pipeline

arXiv
   ↓
download_pdfs()
   ↓
extract_pages()
   ↓
extract_images()
   ↓
generate_text_embeddings()
   ↓
generate_image_embeddings()
   ↓
extract_entities_with_llm()
   ↓
build_graph_nodes_edges()
   ↓
insert_into_spanner()


python backend/pipeline/run_full_ingestion.py


The pipeline will:

• download papers from arXiv  
• extract pages, images, and tables  
• extract biomedical entities with Gemini  
• generate embeddings  
• build the knowledge graph  
• insert everything into Cloud Spanner  

---

# Technologies

- Python
- Google Cloud Spanner
- Vertex AI Gemini
- CLIP embeddings
- Camelot (table extraction)
- PyMuPDF (PDF processing)
- LangChain ArXiv loader



## Graph Visualization

See how to explore the graph in Spanner Studio:

👉 [Graph Visualization Guide](docs/graph-visualization.md)


With ~300 papers your pipeline will still run without it, but batching will make it much faster, cheaper, and safer with APIs and Google Cloud Spanner.

I'll break it down clearly for your current pipeline.

1️⃣ Where batching is actually needed

You have 3 heavy operations:

1. Text embeddings

You call get_text_embedding():

for full paper

for every page

for every caption

for tables

That means thousands of embedding calls.

But Vertex AI text-embedding-004 supports batch input.

Example:

model.get_embeddings(["text1","text2","text3"])

Instead of:

call
call
call
call
2. Spanner writes

Right now you do:

insert_nodes(database, nodes)
insert_nodes(database, page_nodes)
insert_nodes(database, image_nodes)
insert_nodes(database, table_nodes)

for every paper.

For 300 papers this becomes 1200 transactions.

Cloud Spanner performs much better with batch mutations.

3. Image embeddings

Each image call:

get_image_embedding(image)

calls the multimodal model.

If a paper has 20 figures, that is 20 API calls.

Batching images also improves throughput.

2️⃣ Where batching is NOT necessary

These parts are fine as they are:

PDF parsing
extract_pages
extract_images
extract_tables

These are CPU-bound.

Batching won't help.

Entity extraction
extract_entities_with_llm(full_text)

You want one LLM call per paper, so batching doesn't apply.

3️⃣ Biggest performance bottleneck in your pipeline

Right now the slowest parts will be:

1️⃣ embedding generation
2️⃣ Spanner insert transactions

Not the PDF parsing.

4️⃣ Minimal batching change (best approach)

The simplest improvement:

Accumulate all nodes and edges first

Instead of inserting per paper.

Change:

for paper in papers:
   process
   insert

to:

all_nodes = []
all_edges = []

for paper in papers:
    ...
    all_nodes.extend(nodes)
    all_nodes.extend(page_nodes)
    all_nodes.extend(image_nodes)
    all_nodes.extend(table_nodes)

    all_edges.extend(edges)

insert_nodes(database, all_nodes)
insert_edges(database, all_edges)

This will reduce thousands of transactions to a few dozen.

Much better for Google Cloud Spanner.


export PROJECT_ID=search4cure-diabetes
export INSTANCE_ID=diabetes-research-network
export DATABASE_ID=research-graph-db
export REGION=us-central1


## Run Ingestion Pipeline

👉 [Ingestion Pipeline](docs/ingestion-pipeline.md)




## License

MIT License