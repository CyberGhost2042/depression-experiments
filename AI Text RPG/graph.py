import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from IPython.display import display, Image
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage

load_dotenv(".env")


class State(TypedDict):
    """
    Pass in an Annotated List of messages, metadata is add_messages()
    which merges previous interactions with current
    """

    messages: Annotated[list, add_messages]


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS"
)

llm = ChatVertexAI(model_name="gemini-2.0-flash")


def get_user_input(state: State) -> State:
    """
    Returns a TypedDict matching the expected State Schema for the graph
    """
    return {"messages": [state["messages"][-1]]}


def chatbot(state: State) -> State:
    """
    Updates the current passed message history variable aka messages by appending the AI Message
    """
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def print_last_aimessage(state: State):
    """
    Print the last AI Message from the history
    """
    last_msg = state["messages"][-1]
    print("Last AI Message was:", last_msg.content)


builder = StateGraph(state_schema=State)
builder.add_node("human_input", get_user_input)
builder.add_node("chatbot", chatbot)
builder.add_node("printer", print_last_aimessage)

builder.add_edge("human_input", "chatbot")
builder.add_edge("chatbot", "printer")
builder.set_entry_point("human_input")
builder.set_finish_point("printer")


app = builder.compile()
test = {"messages": []}
while True:
    user_inp = input()
    if user_inp == "EXIT":
        break
    else:
        test["messages"].append(HumanMessage(user_inp))
        app.invoke(test)
