

from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langchain_groq import ChatGroq
from graph.state import AgentState
from langchain_core.runnables import RunnableLambda

from langgraph.prebuilt import ToolNode
from langchain_core.messages import ToolMessage
from IPython.display import Image, display
from datetime import datetime

# Define the logic to call the model
def call_model(state: AgentState):
    
    # Get the model
    model = ChatGroq(model="llama-3.3-70b-versatile")

    # Get summary if it exists
    summary = state.get("summary", "")

    # If there is summary, then we add it
    if summary:
        
        # Add summary to system message
        system_message = f"Summary of conversation earlier: {summary}"

        # Append summary to any newer messages
        messages = [SystemMessage(content=system_message)] + state["messages"]
    
    else:
        messages = state["messages"]
    
    response = model.invoke(messages)
    return {"messages": response}

def summarize_conversation_agent(state: AgentState):
    
    # Get the model
    model = ChatGroq(model="llama-3.3-70b-versatile")

    # First, we get any existing summary
    summary = state.get("summary", "")

    # Create our summarization prompt 
    if summary:
        
        # A summary already exists
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
        
    else:
        summary_message = "Create a summary of the conversation above:"

    # Add prompt to our history
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)
    
    return {"summary": response.content, "messages": messages}

def run_llama_model(prompt):
    """Runs the LLM model with retry logic Through Groq"""
    
    llm = ChatGroq(model="llama-3.3-70b-versatile")
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
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )

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