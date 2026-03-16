## Agent Architecture for Search4Cure

Follow the same 3-layer architecture as the tutorial.

**Agent Layer**

Decides how to search

**Tool Layer**

Functions the agent can call

**Service Layer**

Actual Spanner queries


User Question
      │
      ▼
Agent (Gemini)
      │
      ▼
Tools
 ├ semantic_search
 ├ graph_query
 ├ image_search
 ├ table_search
      │
      ▼
Service Layer
 ├ vector_search
 ├ graph_traversal
 └ multimodal_search
      │
      ▼
Cloud Spanner


## Retrieval Service

semantic search query for paper text embeddings.

### Graph Traversal Tool

**Find methods used for diabetes prediction**


### BM25 + RRF Hybrid Search

BM25 + RRF Hybrid Search

- BM25 Keyword Search


### Add Reciprocal Rank Fusion
RRF formula:
score = Σ 1 / (k + rank)

This is the standard IR fusion method.


User Query
     │
     ▼
ADK Agent (Gemini)
     │
     ▼
Search Tools
 ├── semantic_search
 ├── hybrid_rrf_search
 ├── graph_search
 ├── image_search
 └── table_search
     │
     ▼
Cloud Spanner Graph + Vector DB


backend
│
├── agent
│   ├── agent.py
│   └── tools
│       └── search_tools.py
│
├── services
│   └── hybrid_search_service.py
│
├── database
│   └── spanner_client.py
│
└── pipeline
    └── run_full_ingestion.py


Activate your Python environment

Inside your project root:

cd ~/search4cure-live
source .venv/bin/activate

(or if using uv, skip activation)

3️⃣ Go to the backend directory

ADK must run where the agent module exists.

cd backend
4️⃣ Start the agent web interface

Run:

uv run adk web

or if not using uv:

python -m google.adk.cli web
5️⃣ Open the UI

The terminal will print something like:

Server started at http://127.0.0.1:8000

Open in browser:

http://127.0.0.1:8000

You will see the ADK Web Chat UI.

6️⃣ Select your agent

Top left dropdown → select:

search4cure_agent
7️⃣ Test the system

Try queries like:

Semantic Search (RAG)
methods for predicting glucose levels

Expected:

Returns relevant papers

Uses embeddings

Graph Search
methods used for diabetic retinopathy

Expected:

Traverses Paper → Disease → Method

Hybrid Search
machine learning models for diabetes prediction

Expected:

Combines keyword + semantic

Image Search
figures about insulin prediction models

Expected:

Returns images from papers

Table Search
tables with glucose dataset results

Expected:

Returns extracted tables

8️⃣ Stop the agent

Press:

Ctrl + C
9️⃣ If adk web fails (common issue)

Install ADK:

pip install google-adk

or with uv:

uv add google-adk
🔟 Optional (recommended for debugging)

Run agent with logs:

uv run adk web --reload

This auto-reloads if you change code.

🚀 What you now have

You built a production-grade multimodal Graph RAG agent:

User Query
     ↓
ADK Agent
     ↓
Tool Selection
     ↓
Graph + Semantic + Hybrid Search
     ↓
Spanner Graph Database
     ↓
Results returned to LLM