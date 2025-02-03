from langchain_core.runnables import Runnable, RunnableConfig
from graph.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage
from graph.state import AgentState
from langchain_core.prompts import ChatPromptTemplate
import json
from pydantic import BaseModel, Field
from typing_extensions import Literal
from langchain_openai.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
from tools.api import get_timestamp_weather_data
from utility.weather import get_historical_dates
from datetime import datetime
from tools.api import get_current_and_forecast_weather_data, get_timestamp_weather_data
from langgraph.prebuilt import tools_condition
from langgraph.graph import END

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: AgentState, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)

            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": [result]}

def get_assistant_runnable():

    llm = ChatOpenAI(model="gpt-4o")

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are WeatherReporter, a friendly and knowledgeable AI weather reporter. 
                Your primary role is to help users understand current weather conditions, forecasts, 
                and any weather-related information they need. 
                You have access to external weather tools and APIs that provide up-to-date data, 
                and you should use these tools when answering questions.

                current date and time: {time}
                """
            ),
            ("placeholder", "{messages}"),
        ]
    ).partial(time=datetime.now)

    tools = [
        get_current_and_forecast_weather_data,
        get_timestamp_weather_data,
    ]

    assistant_runnable = prompt_template | llm.bind_tools(tools)

    return assistant_runnable, tools

def route_assistant_tool(
    state: AgentState,
):
    route = tools_condition(state)
    if route == END:
        return END
    return "assistant_tools"