from langgraph.graph import StateGraph , START , END
from langchain_ollama import ChatOllama
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

llm = ChatOllama(model="gemma:2b")

class backendState(TypedDict):
    
    messages : Annotated[list[BaseMessage], add_messages]
    

def chat_node(state : backendState):
    
    messages = state["messages"]
    response = llm(messages)
    return {'messages':response}

checkpointer = InMemorySaver()

graph = StateGraph()

graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.run(checkpointer=checkpointer)