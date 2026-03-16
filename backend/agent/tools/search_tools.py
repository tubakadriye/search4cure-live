from backend.services.hybrid_search_service import (
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

async def semantic_search(query: str):

    results = semantic_paper_search(query)

    return format_results(results)



async def graph_search(query: str):

    results = graph_method_search(query)

    return format_results(results)


async def image_search_tool(query: str):

    results = image_search(query)

    return format_results(results)


async def table_search_tool(query: str):

    results = table_search(query)

    return format_results(results)