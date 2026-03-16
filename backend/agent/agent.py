from google.adk.agents import Agent

from backend.agent.tools.search_tools import (
    hybrid_rrf_search,
    page_search_tool,
    semantic_search,
    graph_search,
    image_search_tool,
    table_search_tool
)

agent = Agent(
    name="search4cure_agent",
    model="gemini-1.5-pro",
    instruction="""
You are a biomedical research assistant helping researchers explore diabetes literature.

Search tools:

semantic_search
Use when the user asks for similar concepts or vague ideas.

Example:
"methods for glucose prediction"

hybrid_rrf_search
Default search combining semantic and keyword search.

Example:
"papers about glucose monitoring models"

graph_search
Use when the user asks about relationships between entities.

Example:
"methods used for diabetic retinopathy"

page_search_tool
Use when user asks for specific explanations or sections.

Example:
"how does CGM prediction work"

image_search_tool
Retrieve figures from research papers.

table_search_tool
Retrieve tables from research papers.
""",
    tools=[
    hybrid_rrf_search,
    semantic_search,
    graph_search,
    page_search_tool,
    image_search_tool,
    table_search_tool
]
)