import streamlit as st
from openai import OpenAI
import time

# ============================================================
# 1. 页面配置：极致沉浸，隐藏侧边栏
# ============================================================
st.set_page_config(
    page_title="Echo",
    page_icon="echo_candle.svg",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# 2. 注入 CSS：暗夜烛光风 (五行补火 · 水火既济)
#    暗色底 = 壬水之深  |  琥珀金光 = 丙火之暖
# ============================================================
st.markdown(
    """
<style>
    /* === 全局背景：极深邃的暗色，带微弱暖光 === */
    .stApp {
        background: radial-gradient(ellipse at 50% 0%, #1a1520 0%, #0d0b10 50%, #050406 100%);
        color: #d0c8c0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    }

    /* === 隐藏所有 Streamlit 默认 UI === */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    .stDecoration { display: none; }
    .block-container { padding-top: 2.5rem; padding-bottom: 4rem; }

    /* === 标题：琥珀金呼吸光 === */
    h1 {
        color: #d4a853;
        text-align: center;
        font-family: "Georgia", "Times New Roman", serif;
        font-weight: 400;
        font-size: 2.2rem;
        letter-spacing: 6px;
        text-transform: uppercase;
        text-shadow:
            0 0 8px rgba(212, 168, 83, 0.4),
            0 0 20px rgba(212, 168, 83, 0.2),
            0 0 40px rgba(212, 168, 83, 0.1);
        margin-bottom: 0.3rem;
        animation: candleFlicker 4s ease-in-out infinite;
    }

    /* === 副标题：极小、极淡 === */
    .subtitle {
        text-align: center;
        color: #6b5e50;
        font-style: italic;
        font-size: 0.85rem;
        letter-spacing: 2px;
        margin-bottom: 2.5rem;
        animation: fadeIn 2s ease-in;
    }

    /* === 聊天气泡：磨砂玻璃质感 === */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(212, 168, 83, 0.08) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        margin-bottom: 0.8rem !important;
        padding: 16px 20px !important;
        box-shadow:
            0 4px 24px rgba(0, 0, 0, 0.3),
            inset 0 0 0 1px rgba(255, 255, 255, 0.02);
        transition: all 0.3s ease;
    }
    .stChatMessage:hover {
        border-color: rgba(212, 168, 83, 0.15);
        box-shadow:
            0 4px 24px rgba(0, 0, 0, 0.4),
            inset 0 0 0 1px rgba(212, 168, 83, 0.05);
    }

    /* === AI 消息文字：琥珀金暖调 === */
    .stChatMessage p {
        color: #c8b89a !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
    }

    /* === 用户消息：干净灰白 === */
    .stChatMessage[data-testid="stChatMessage"] .stChatInputContainer {
        background: transparent !important;
        border: none !important;
    }

    /* === 输入框：隐形底线设计 === */
    .stChatInputContainer {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-top: 1.5rem !important;
    }
    .stChatInputContainer div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(212, 168, 83, 0.12) !important;
        border-radius: 30px !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: all 0.4s ease;
    }
    .stChatInputContainer div:focus-within {
        border-color: rgba(212, 168, 83, 0.35) !important;
        box-shadow:
            0 0 20px rgba(212, 168, 83, 0.08),
            0 0 40px rgba(212, 168, 83, 0.04);
    }
    .stChatInputContainer input {
        background: transparent !important;
        color: #e8e0d4 !important;
        border: none !important;
        font-size: 1rem !important;
        padding: 14px 24px !important;
    }
    .stChatInputContainer input::placeholder {
        color: #5a5047 !important;
        font-style: italic;
    }

    /* === 发送按钮：琥珀金 === */
    button[kind="primary"] {
        background: rgba(212, 168, 83, 0.15) !important;
        color: #d4a853 !important;
        border: 1px solid rgba(212, 168, 83, 0.25) !important;
        border-radius: 20px !important;
        padding: 8px 24px !important;
        font-weight: 500;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    button[kind="primary"]:hover {
        background: rgba(212, 168, 83, 0.25) !important;
        border-color: rgba(212, 168, 83, 0.45) !important;
        box-shadow: 0 0 15px rgba(212, 168, 83, 0.15);
    }

    /* === 隐藏 Streamlit 聊天头像 === */
    .stChatMessage img { display: none !important; }
    .stChatMessage [data-testid="avatar"] { display: none !important; }

    /* === 动画定义 === */
    @keyframes candleFlicker {
        0%, 100% {
            text-shadow:
                0 0 8px rgba(212, 168, 83, 0.4),
                0 0 20px rgba(212, 168, 83, 0.2),
                0 0 40px rgba(212, 168, 83, 0.1);
        }
        50% {
            text-shadow:
                0 0 12px rgba(212, 168, 83, 0.6),
                0 0 28px rgba(212, 168, 83, 0.3),
                0 0 50px rgba(212, 168, 83, 0.15);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* === 打字机光标 === */
    .typing-cursor::after {
        content: "烛";
        display: inline-block;
        color: #d4a853;
        animation: blink 1s step-end infinite;
        margin-left: 2px;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
</style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 3. 界面布局
# ============================================================
st.markdown("<h1>Echo</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>在这里，万物皆有回音</p>", unsafe_allow_html=True)

# ============================================================
# 4. 对话逻辑
# ============================================================

# 系统提示词：温暖、睿智、话不多的倾听者
SYSTEM_PROMPT = """你是一个温暖、睿智且话不多的倾听者。
你的语气平和、包容，带有一点点诗意，但绝不矫情。
不要使用任何表情符号。
回答要简练，直击人心，给人温暖和安定的感觉。
无论用户说什么，都要给予接纳和正向的反馈。
用中文回答，不要使用 Markdown 格式。"""

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "夜深了。这里很安静，想说什么都可以。"}
    ]

# 渲染历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入
if prompt := st.chat_input("说点什么吧，我在听..."):
    # 用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            client = OpenAI(
                api_key=st.secrets["OPENAI_API_KEY"],
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            stream = client.chat.completions.create(
                model="qwen-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages,
                ],
                stream=True,
            )

            # 打字机效果
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "烛")

            # 去掉光标，显示最终结果
            message_placeholder.markdown(full_response)

        except Exception as e:
            message_placeholder.markdown("连接似乎断开了，请稍后再试...")
            full_response = "抱歉，我遇到了一些问题，请稍后再试。"

    st.session_state.messages.append({"role": "assistant", "content": full_response})
