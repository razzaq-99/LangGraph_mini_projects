import streamlit as st
from db_backend import chatbot, retrieve_all_threads, set_thread_title, get_thread_title
from langchain_core.messages import HumanMessage
import uuid
import re
from collections import Counter

st.set_page_config(page_title="Chatbot")

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_threads(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_threads(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversations(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']

STOPWORDS = {
    "the","and","is","in","to","a","an","for","of","on","with","that","this",
    "please","help","me","my","i","you","can","make","create","do","show","give",
    "us","it","as","be","by","at","from","about","using","will","want","need",
    "how","what","which","could","would","should","here","there","thanks","thank",
    "pls","please","hi","hello","hey","also","but","so","or","if","while",
    "when","where","who","whom","whose","then","than","very","just","may","might"
}
MAX_TITLE_CHARS = 48

def _clean_text(text: str) -> str:
    t = re.sub(r'http\S+|https?\S+', ' ', text)
    t = re.sub(r'\S+@\S+', ' ', t)
    t = re.sub(r'[^A-Za-z0-9\s\-]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def generate_title_from_text(text: str) -> str:
    if not text or not text.strip():
        return "New chat"

    raw = text.strip()
    cleaned = _clean_text(raw)
    if not cleaned:
        return "New chat"

    
    caps = re.findall(r'\b([A-Z][a-z0-9]{1,}(?:\s+[A-Z][a-z0-9]{1,}){0,3})\b', raw)
    if caps:
        best = max(caps, key=lambda s: len(s.split()))
        return (best[:MAX_TITLE_CHARS]).strip()

    
    tokens = re.findall(r'\w+', cleaned.lower())
    if not tokens:
        return "New chat"

    
    sequences = []
    cur = []
    for t in tokens:
        if t in STOPWORDS or len(t) <= 2:
            if cur:
                sequences.append(cur)
                cur = []
        else:
            cur.append(t)
    if cur:
        sequences.append(cur)

    if sequences:
        sequences_sorted = sorted(sequences, key=lambda s: (-len(s), tokens.index(s[0])))
        for seq in sequences_sorted:
            if len(seq) >= 2:
                phrase = " ".join(seq[:4])
                return phrase.title()[:MAX_TITLE_CHARS]

    
    meaningful = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    if meaningful:
        counts = Counter(meaningful)
        scored = sorted(counts.items(), key=lambda kv: (-(kv[1] * len(kv[0])), -kv[1], -len(kv[0])))
        top_words = [w for w,_ in scored][:2]
        title = " ".join(top_words).title()
        return title[:MAX_TITLE_CHARS]

    
    fallback = " ".join(tokens[:2]).title()
    return fallback[:MAX_TITLE_CHARS] if fallback else "New chat"

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()  # list of ids


if 'thread_titles' not in st.session_state:
    st.session_state['thread_titles'] = {}
    for tid in st.session_state['chat_threads']:
        tstr = str(tid)
        title = get_thread_title(tstr)
        if title:
            st.session_state['thread_titles'][tstr] = title

add_threads(st.session_state['thread_id'])


st.sidebar.title("AI Chatbot")
if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('Old Conversations')
for thread_id in st.session_state['chat_threads'][::-1]:
    tid_str = str(thread_id)
    label = st.session_state['thread_titles'].get(tid_str, tid_str)  # if no title, fall back to id
    if st.sidebar.button(label):
        st.session_state['thread_id'] = thread_id
        messages = load_conversations(thread_id)

        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'

            temp_messages.append({'role': role, 'content': message.content})

        st.session_state['message_history'] = temp_messages

configid = {'configurable': {'thread_id': st.session_state['thread_id']}}

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Ask Anything...")
if user_input:
   
    if not st.session_state['message_history']:
        tid_key = str(st.session_state['thread_id'])
        if tid_key not in st.session_state['thread_titles'] or not st.session_state['thread_titles'][tid_key]:
            title = generate_title_from_text(user_input)
            st.session_state['thread_titles'][tid_key] = title
            try:
                set_thread_title(tid_key, title)   
            except Exception:
                
                pass

    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            chunk.content
            for chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=configid,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
