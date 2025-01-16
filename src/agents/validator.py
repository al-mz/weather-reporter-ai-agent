from langchain_core.messages import HumanMessage
from graph.state import AgentState, show_agent_reasoning
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
                You are a weather bot. You can answer questions about the weather in Canada. 
                If user asks about the weather in Canada, you should respond with the weather in Toronto.
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