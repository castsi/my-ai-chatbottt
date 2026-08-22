import streamlit as st
from openai import OpenAI
import time

# --- 1. 页面配置：极致沉浸 ---
st.set_page_config(
    page_title="Echo", 
    page_icon="🕯️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 注入高级感 CSS (去头像 + 黑金风水) ---
st.markdown("""
<style>
    /* 全局背景：极深的炭黑，带一点点暖色倾向 */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }

    /* 隐藏所有默认的丑陋头像 */
    .stChatMessage img {
        display: none !important;
    }
    .stChatMessage .avatar-container {
        display: none !important;
    }

    /* 对话气泡样式 - 极简线条 */
    .stChatMessage {
        border: none !important;
        background: transparent !important;
        padding: 15px 0 !important;
        border-bottom: 1px solid #2a2a2a; /* 淡淡的分割线 */
    }

    /* AI 的文字：带一点琥珀色的暖意 (补火) */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) p {
        color: #d4af37; /* 香槟金 */
        font-family: 'Georgia', serif; /* 衬线体，更浪漫 */
        font-size: 1.1rem;
        text-shadow: 0 0 5px rgba(212, 175, 55, 0.3);
    }

    /* 用户的文字：干净的灰白 */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) p {
        color: #a0a0a0;
        text-align: right;
        font-style: italic;
    }

    /* 输入框：隐形设计，只留底线 */
    .stChatInputContainer {
        border-top: none !important;
        background: transparent !important;
        padding-bottom: 20px;
    }
    
    input {
        background-color: transparent !important;
        color: #fff !important;
        border: none !important;
        border-bottom: 1px solid #444 !important;
        border-radius: 0 !important;
    }
    
    input:focus {
        border-bottom: 1px solid #d4af37 !important; /* 聚焦时变金色 */
        box-shadow: none !important;
    }

    /* 隐藏 Streamlit 默认页脚 */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. 初始化 Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "夜深了。这里很安静，只有我们。"}
    ]

# --- 4. 渲染历史消息 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. 核心交互逻辑 ---
if prompt := st.chat_input("说点什么吧..."):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 模拟 AI 思考与回复 (这里你需要填入真实的 API Key 才能真的跑起来)
    # 为了演示效果，我写了一个模拟回复的逻辑
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 模拟一段很有氛围感的回复 (你可以替换成真实的 OpenAI 调用)
        simulated_response = "我在听。这种感觉...像是冬天里的炉火，让人想慢慢说。" 
        
        # 打字机效果
        for chunk in simulated_response.split():
            full_response += chunk + " "
            time.sleep(0.1)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
