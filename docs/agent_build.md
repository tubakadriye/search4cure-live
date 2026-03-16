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