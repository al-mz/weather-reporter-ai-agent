from langchain_core.messages import HumanMessage
from src.graph.state import AgentState, show_agent_reasoning
from langchain_core.prompts import ChatPromptTemplate
import json

def validator_agent(state: AgentState):
    "Make sure user request is for Canada and devide the request into 3 parts"

    # Get the latest message
    message = state['messages'][-1]
    
    # Create the prompt template
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a weather
                """,
            ),
            (
                "human",
                """
                What is the weather in Toronto?
                """,
            ),
        ]
    )