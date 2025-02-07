from datetime import datetime

from geopy.geocoders import Nominatim
from IPython.display import Image, display
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt import ToolNode


def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks([RunnableLambda(handle_tool_error)], exception_key="error")


def save_workflow_graph(workflow, filename="workflow_graph.png"):
    """
    Generate and save a graph of the given workflow.

    Args:
        workflow: The workflow to be depicted.
        filename: The name of the file to save the graph as.
    """
    try:
        graph = workflow.get_graph(xray=True).draw_mermaid_png()
        with open(filename, "wb") as f:
            f.write(graph)
        display(Image(filename))
    except Exception as e:
        print(f"An error occurred while generating the graph: {e}")


def is_valid_timestamp(timestamp):
    try:
        datetime.fromtimestamp(timestamp)
        return True
    except (OSError, ValueError):
        return False


def get_lat_lon(city_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None
