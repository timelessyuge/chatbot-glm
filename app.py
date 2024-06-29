from registry import *
from utils import chat

import streamlit as st
import time




model = "glm-4"

system_message = "你是一个智能生活小助手，请回答用户的问题。"

history = [{"role": "system", "content": system_message}]


st.set_page_config(
    page_title="AI chatbot",
    layout="centered",
    initial_sidebar_state="expanded",  # collapsed
)

st.title("AI智能生活助手")
st.markdown("解答您日常提问，请在下方的对话栏输入：")

with st.sidebar:
    temperature = st.slider("temperature", 0.01, 0.99, 0.60, step=0.01)
    top_p = st.slider("top_p", 0.01, 0.99, 0.80, step=0.01)
    max_tokens = st.slider("max_tokens", 128, 1024, 384, step=32)
    output_speed = st.slider("words/sec", 0, 1000, 0, step=100)


user_input = st.chat_input("chat with AI assistant:🎉")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.empty()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        message_content = message["content"]
        if isinstance(message_content, tuple):
            url, _ = message_content
            st.image(url, width=400)
        else:
            st.write(message_content)

if user_input:
    sleeptime = output_speed**-1 if output_speed > 0 else 0

    history.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    bot_response = chat(
        client=client,
        model=model,
        history=history,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        tools=tools,
    )

    with st.chat_message("assistant"):

        if isinstance(bot_response, pd.DataFrame):
            bot_response_str = bot_response.to_string()
            # with st.chat_message("assistant"):
            st.write(bot_response)

        elif isinstance(bot_response, tuple):
            url, bot_response_str = bot_response
            st.image(url, width=400)
        else:
            bot_response_str = bot_response
            # with st.chat_message("assistant"):
            # st.markdown(bot_response)
            placeholder = st.empty()
            full_response = ""

            for word in bot_response:
                full_response += word
                time.sleep(sleeptime)
                placeholder.markdown(full_response)

    history.append({"role": "assistant", "content": bot_response_str})
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
