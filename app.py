import streamlit as st
from openai import OpenAI

# --- 1. 页面配置：浪漫星空风 ---
st.set_page_config(
    page_title="紫夜星轨 | Starry AI", 
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 注入浪漫 CSS (紫气东来 + 玫瑰金) ---
st.markdown("""
<style>
    /* 全局背景：深邃的星空紫渐变 */
    .stApp {
        background: radial-gradient(circle at center, #2b1b40 0%, #0f0c1b 100%);
        color: #e8d5f5; /* 柔和的淡紫白色字体 */
    }

    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 标题：玫瑰金发光效果 */
    h1 {
        color: #f8e8ee;
        text-align: center;
        font-family: 'Georgia', serif; /* 优雅的衬线字体 */
        text-shadow: 0 0 15px rgba(255, 182, 193, 0.6);
        margin-bottom: 5px;
    }

    /* 副标题样式 */
    .sub-header {
        text-align: center;
        color: #bca0d8;
        font-style: italic;
        margin-bottom: 30px;
        font-size: 1.1rem;
    }

    /* 输入框：浪漫圆角 + 紫色边框 */
    .stChatInput input {
        background-color: rgba(43, 27, 64, 0.8);
        color: #fff;
        border: 1px solid #9d7bbf;
        border-radius: 25px !important;
        padding: 15px 20px;
        font-size: 1rem;
    }
    .stChatInput input:focus {
        border-color: #ffb6c1 !important;
        box-shadow: 0 0 15px rgba(255, 182, 193, 0.4);
    }

    /* 聊天气泡：半透明紫 */
    .stChatMessage {
        background-color: rgba(80, 50, 120, 0.4);
        border: 1px solid rgba(157, 123, 191, 0.3);
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }

    /* 按钮样式 */
    button[kind="primary"] {
        background-color: #9d7bbf !important;
        color: #fff !important;
        border: none !important;
        border-radius: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 界面布局 ---
st.title(" 紫夜星轨")
st.markdown("<p class='sub-header'> 无论是摩羯的沉稳，还是天蝎的深情，在这里，你的每一个念头都有回音。</p>", unsafe_allow_html=True)

# 初始化 API 客户端 (阿里云通义千问)
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. 对话逻辑 (带打字机效果) ---
if prompt := st.chat_input("在这里留下你的心事..."):
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 显示 AI 思考中
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 调用 API
        stream = client.chat.completions.create(
            model="qwen-turbo", 
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True
        )
        
        # 模拟打字机效果
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "")
        
        # 最终显示
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
