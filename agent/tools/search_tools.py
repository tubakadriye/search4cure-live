from backend.services.hybrid_search_service import (
    hybrid_rrf_search,
    page_semantic_search,
    semantic_paper_search,
    graph_method_search,
    image_search,
    table_search
)

def format_results(results):

    if not results:
        return "No results found."

    formatted = []

    for r in results:
        formatted.append(str(r))

    return "\n".join(formatted)





# ---------------------
# Tools used by agent
# ---------------------

async def semantic_search(query: str, limit: int = 10) -> str:
    """
    Force semantic (RAG) search using embeddings.

    Best for:
    - Conceptual queries
    - Similarity search
    - Unknown terminology
    """

    try:
        results = semantic_paper_search(query, limit)

        if not results:
            return "No relevant papers found."

        formatted = []

        for r in results:
            formatted.append(
                f"Paper: {r['title']} | Method: {r.get('method')} | Disease: {r.get('disease')} | Distance: {r['distance']}"
            )

        return "\n".join(formatted)

    except Exception as e:
        return f"Error in semantic search: {str(e)}"



async def graph_search(query: str):

    results = graph_method_search(query)

    return format_results(results)


async def image_search_tool(query: str):

    results = image_search(query)

    return format_results(results)


async def table_search_tool(query: str):

    results = table_search(query)

    return format_results(results)


async def page_search_tool(query: str):

    results = page_semantic_search(query)

    return format_results(results)

# ---------------------
# Tools used by agent
# ---------------------

async def hybrid_rrf_search_tool(query: str, limit: int = 10) -> str:
    """
    Default hybrid RRF search combining semantic + keyword search.

    Best for:
    - General queries about papers
    - Combining similarity and keyword-based ranking
    """
    try:
        results = hybrid_rrf_search(query, limit=limit)

        if not results:
            return "No relevant papers found."

        formatted = []
        for r in results:
            formatted.append(f"Paper: {r['title']} | Score: {r['score']:.4f}")

        return "\n".join(formatted)

    except Exception as e:
        return f"Error in hybrid RRF search: {str(e)}"