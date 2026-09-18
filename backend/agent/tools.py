from backend.rag.vector_search import vector_search
from backend.graph.graph_search import graph_search

def run_vector_tool(query: str):
    return vector_search(query)

def run_graph_tool(entity: str):
    return graph_search(entity)
