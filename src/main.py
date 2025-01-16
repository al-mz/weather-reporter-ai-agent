from langgraph.graph import END, StateGraph
from graph.state import AgentState

def start(state: AgentState):
    """Initialize the workflow with the input message."""
    return state