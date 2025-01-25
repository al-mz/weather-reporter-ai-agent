import os
from langchain_core.messages import HumanMessage
from graph.state import AgentState, show_agent_reasoning
from tools.api import get_weather_data

import json

api_key = os.environ.get("OPENWEATHER_API_KEY")

def hourly_agent(state: AgentState):
    "Make sure user request is for Canada and devide the request into 3 parts"

    # Get the latest message
    data = state['data']


