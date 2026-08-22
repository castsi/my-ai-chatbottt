import streamlit as st
import os
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# 设置页面标题
st.set_page_config(page_title="我的 AI 助手", page_icon="🤖")

# 初始化 AI 模型（使用 Ollama 本地模型）
@st.cache_resource
def load_model():
    return Ollama(model="qwen")  # 这里的模型名根据你ollama装的模型改

model = load_model()

# 聊天历史
st.title("🤖 我的 AI 助手")
st.caption("Powered by Ollama + Streamlit")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示聊天历史
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 用户输入
if prompt := st.chat_input("你想问什么？"):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # AI 回复
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = model.invoke(prompt)
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})