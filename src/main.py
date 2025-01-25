from langgraph.graph import END, StateGraph
from graph.state import AgentState
from agents.master import master_agent
from agents.hourly import hourly_agent
from agents.current import current_agent
from langchain_core.messages import HumanMessage
from typing_extensions import Literal

import os, getpass

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")
_set_env("GROQ_API_KEY")
_set_env("OPENWEATHER_API_KEY")

# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

def start(state: AgentState):
    """Initialize the workflow with the input message."""
    return state

def decision_weather(state: AgentState) -> Literal["current_agent"]:

    # retreive the latest message
    decision = state["data"]['user_request']['decision']

    if decision == "current":
        return "current_agent"
    

def create_workflow():
    """Create the workflow with selected analysts."""

    # add nodes
    workflow = StateGraph(AgentState)
    workflow.add_node("start_node", start)
    workflow.add_node("master_agent", master_agent)
    workflow.add_node("current_agent", current_agent)
    workflow.add_node("hourly_agent", hourly_agent)

    # add edges
    workflow.add_edge("start_node", "master_agent")
    workflow.add_conditional_edges("master_agent", decision_weather)
    workflow.add_edge("master_agent", END)

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