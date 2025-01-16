from langgraph.graph import END, StateGraph
from graph.state import AgentState
from agents.validator import validator_agent
from langchain_core.messages import HumanMessage

# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

def start(state: AgentState):
    """Initialize the workflow with the input message."""
    return state

def create_workflow(selected_analysts:list):
    """Create the workflow with selected analysts."""
    workflow = StateGraph(AgentState)
    workflow.add_node("start_node", start)

    # Default to all analysts if none selected
    if selected_analysts is None:
        selected_analysts = [
            "validator_agent", 
            # "fundamentals_analyst", 
            # "sentiment_analyst", 
            # "valuation_analyst"
            ]

    # Dictionary of all available analysts
    analyst_nodes = {
        "validator_agent": ("validator_agent", validator_agent),
        # "fundamentals_analyst": ("fundamentals_agent", fundamentals_agent),
        # "sentiment_analyst": ("sentiment_agent", sentiment_agent),
        # "valuation_analyst": ("valuation_agent", valuation_agent),
    }

    # Add selected analyst nodes
    for analyst_key in selected_analysts:
        node_name, node_func = analyst_nodes[analyst_key]
        workflow.add_node(node_name, node_func)
        workflow.add_edge("start_node", node_name)
    
    workflow.add_edge("validator_agent", END)

    workflow.set_entry_point("start_node")
    return workflow

def run_workflow(agent, input_message):
    """Run the workflow with the input message."""
    final_state = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="Make trading decisions based on the provided data.",
                )
            ],
            # "data": {
            #     "tickers": tickers,
            #     "portfolio": portfolio,
            #     "start_date": start_date,
            #     "end_date": end_date,
            #     "analyst_signals": {},
            # },
            "metadata": {
                "show_reasoning": show_reasoning,
            },
        },
    )

if __name__ == "__main__":

    # Create the workflow with selected analysts
    workflow = create_workflow(["validator_agent"])
    app = workflow.compile()