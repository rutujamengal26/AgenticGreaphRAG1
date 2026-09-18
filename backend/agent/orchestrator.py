from backend.agent.state import AgentState
from backend.agent.tools import run_vector_tool, run_graph_tool

def run_agent(query: str):
    state = AgentState(query=query)
    vector_results = run_vector_tool(query)
    graph_results = run_graph_tool(query)
    state.history.append({"vector": vector_results, "graph": graph_results})
    return state
