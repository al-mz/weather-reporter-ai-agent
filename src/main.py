import getpass
import os

import gradio as gr
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from agents.assistant import Assistant, get_assistant_runnable, route_assistant_tool
from graph.state import AgentState
from utility.utils import create_tool_node_with_fallback


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("OPENAI_API_KEY")
_set_env("GROQ_API_KEY")
_set_env("OPENWEATHER_API_KEY")


def create_workflow():
    """Create the workflow with selected analysts."""

    # Build the workflow
    assistant_runnable, tools = get_assistant_runnable()

    workflow = StateGraph(AgentState)
    workflow.add_node("assistant", Assistant(assistant_runnable))
    workflow.add_node("assistant_tools", create_tool_node_with_fallback(tools))

    # add edges
    workflow.add_edge(START, "assistant")
    workflow.add_conditional_edges("assistant", route_assistant_tool, ["assistant_tools", END])
    workflow.add_edge("assistant_tools", "assistant")

    return workflow


def run_workflow(input_message):
    """Run the workflow with the input message."""

    ai_response = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=input_message,
                )
            ],
        },
        config,
    )

    return ai_response


def chatbot_interface(user_input, history):
    ai_response = run_workflow(user_input)

    return ai_response["messages"][-1].content


def chat_with_product_data():
    with gr.Blocks(title="AI Shop Assistant", theme=gr.themes.Soft(), fill_width=True) as demo:
        chatbot = gr.Chatbot(
            value=[
                [
                    None,
                    "Hi, I'm your weather ai assistant. Ask me about the weather in any city!",
                ]
            ],
            placeholder="**Ask me about products you want to buy!**",
            height=800,
            # label=f"{self.shop_config['settings']['name']} ShopAI Assistant",
            # avatar_images=("/app/assets/user-avatar.png", "/app/assets/beisat-logo.png"),
        )
        gr.ChatInterface(
            fn=chatbot_interface,
            chatbot=chatbot,
        )

    demo.launch()


if __name__ == "__main__":

    # Create a memory saver
    memory = MemorySaver()
    config = {"configurable": {"thread_id": "2"}}

    # Create the workflow with selected analysts
    workflow = create_workflow()
    agent = workflow.compile(checkpointer=memory)

    # chat with the assistant
    chat_with_product_data()
