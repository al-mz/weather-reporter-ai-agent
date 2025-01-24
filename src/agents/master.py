from langchain_core.messages import HumanMessage
from graph.state import AgentState, show_agent_reasoning
from langchain_core.prompts import ChatPromptTemplate
import json
from pydantic import BaseModel, Field
from typing_extensions import Literal
from langchain_openai.chat_models import ChatOpenAI

# Define the output model for the LLM
class MasterAgentOutput(BaseModel):
    decision: Literal["hourly", "daily", "historical"]
    reasoning: str = Field(description="Reasoning for the decision")

def make_decision(prompt: str):
    """Attempts to get a decision from the LLM with retry logic"""
    llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(
        MasterAgentOutput,
        method="function_calling",
    )
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = llm.invoke(prompt)
            return result
        except Exception as e:
            print(f"Error - retry {attempt + 1}/{max_retries}")
            if attempt == max_retries - 1:
                # On final attempt, return a safe default
                return None

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
                You are a weather reporter bot. 
                Your responsibility is to detemine whether the user is asking for one of the hourly, daily, or historical weather data.
                """,
            ),
            (
                "human",
                """
                Question: {user_message}

                Return a decision on whether the user is asking for hourly, daily, or historical weather data.
                in this format:
                {{
                    "decision": "hourly",
                    "reasoning": "string"
                }}
                Only return the one that is most likely.
                """,
            ),
        ]
    )

    # invoke template
    prompt = template.invoke(
        {
            "user_message": message.content,
        }
    )

    # Get the decision from the LLM
    decision = make_decision(prompt)

    # create master agent message
    message = HumanMessage(
        content= json.dumps(decision.dict(), indent=2),
        name="master_agent",
    )

    return {
        "messages": state["messages"] + [message],
    }