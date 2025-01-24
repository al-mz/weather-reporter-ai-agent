from langgraph.graph import END, StateGraph
from graph.state import AgentState
from agents.master import validator_agent
from langchain_core.messages import HumanMessage

import os, getpass

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")

# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

def start(state: AgentState):
    """Initialize the workflow with the input message."""
    return state

def create_workflow():
    """Create the workflow with selected analysts."""
    workflow = StateGraph(AgentState)
    workflow.add_node("start_node", start)

    # # Dictionary of all available analysts
    # analyst_nodes = {
    #     "validator_agent": ("validator_agent", validator_agent),
    #     # "fundamentals_analyst": ("fundamentals_agent", fundamentals_agent),
    #     # "sentiment_analyst": ("sentiment_agent", sentiment_agent),
    #     # "valuation_analyst": ("valuation_agent", valuation_agent),
    # }

    # # Add selected analyst nodes
    # for analyst_key, analyst_value in analyst_nodes.items():
    #     node_name, node_func = analyst_nodes[analyst_key]
    #     workflow.add_node(node_name, node_func)
    #     workflow.add_edge("start_node", node_name)
    workflow.add_node("validator_agent", validator_agent)
    
    workflow.add_edge("start_node", "validator_agent")
    workflow.add_edge("validator_agent", END)

    workflow.set_entry_point("start_node")
    return workflow

def run_workflow(agent, input_message):
    """Run the workflow with the input message."""
    final_state = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=input_message,
                )
            ],
            # "data": {
            #     "tickers": tickers,
            #     "portfolio": portfolio,
            #     "start_date": start_date,
            #     "end_date": end_date,
            #     "analyst_signals": {},
            # },
            # "metadata": {
            #     "show_reasoning": show_reasoning,
            # },
        },
    )

    return final_state["messages"][-1].content

if __name__ == "__main__":

    # Create the workflow with selected analysts
    workflow = create_workflow()
    agent = workflow.compile()

    # Run the workflow with the input message
    run_workflow(agent, "How's the weather in Toronto right now?")