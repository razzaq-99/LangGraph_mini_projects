import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

st.set_page_config(page_title="Chatbot")

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    
    
st.sidebar.title("AI Chatbot")
if st.sidebar.button('New Chat'):
    reset_chat()
st.sidebar.header('Old Conversations')
st.sidebar.text(st.session_state['thread_id'])
    

configid = {'configurable': {'thread_id': st.session_state['thread_id']}}

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Ask Anything...")
if user_input:
    
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
