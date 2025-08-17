from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage
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


connection = sqlite3.connect("chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=connection)


connection.execute("""
CREATE TABLE IF NOT EXISTS thread_meta (
    thread_id TEXT PRIMARY KEY,
    title TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
)
""")
connection.commit()

graph = StateGraph(BackendState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)


def set_thread_title(thread_id: str, title: str) -> None:
    """Insert or update a saved human-readable title for a thread."""
    connection.execute("""
        INSERT INTO thread_meta (thread_id, title, created_at, updated_at)
        VALUES (?, ?, datetime('now'), datetime('now'))
        ON CONFLICT(thread_id) DO UPDATE SET
            title=excluded.title,
            updated_at=datetime('now')
    """, (str(thread_id), title))
    connection.commit()

def get_thread_title(thread_id: str):
    """Return stored title or None."""
    cur = connection.execute("SELECT title FROM thread_meta WHERE thread_id = ?", (str(thread_id),))
    row = cur.fetchone()
    return row[0] if row and row[0] else None


def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
