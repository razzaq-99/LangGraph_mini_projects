from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

llm = ChatOllama(model="gemma:2b")

class BackendState(TypedDict):
    
    messages: Annotated[List[BaseMessage], add_messages]

def chat_node(state: BackendState) -> dict:
    msgs: List[BaseMessage] = state["messages"]
    ai_msg = llm.invoke(msgs)  
    
    return {"messages": [ai_msg]}

connection = sqlite3.connect("chatbot.db", check_same_thread = False)

checkpointer = SqliteSaver(conn=connection)


graph = StateGraph(BackendState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


chatbot = graph.compile(checkpointer=checkpointer)