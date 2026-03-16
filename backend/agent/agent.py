from google.adk.agents import Agent

from backend.agent.tools.search_tools import (
    semantic_search,
    graph_search,
    image_search_tool,
    table_search_tool
)

agent = Agent(
    name="search4cure_agent",
    model="gemini-1.5-pro",
    instruction="""
You are a biomedical research assistant.

You help researchers explore diabetes research papers.

Use the tools when necessary:

semantic_search → find relevant research papers
graph_search → explore relationships between diseases and methods
image_search_tool → retrieve figures from papers
table_search_tool → retrieve tables from papers
""",
    tools=[
        semantic_search,
        graph_search,
        image_search_tool,
        table_search_tool
    ]
)