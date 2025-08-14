import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Chatbot")

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

configid = {'configurable': {'thread_id': '1'}}

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("What's your question?")
if user_input:
    
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            chunk.content 
            for chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=configid,        # ✅ correct way
                stream_mode='messages'
            )
        )

    
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
