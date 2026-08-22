import streamlit as st
from openai import OpenAI

# ============================================================
# 1. 页面配置
# ============================================================
st.set_page_config(
    page_title="Echo",
    page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCIgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0Ij4KICA8ZGVmcz4KICAgIDxyYWRpYWxHcmFkaWVudCBpZD0iZmxhbWVDb3JlIiBjeD0iNTAlIiBjeT0iNjAlIiByPSI1MCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojZmZmOGU3O3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjQwJSIgc3R5bGU9InN0b3AtY29sb3I6I2Y1ZDc4MDtzdG9wLW9wYWNpdHk6MSIgLz4KICAgICAgPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjojZDRhODUzO3N0b3Atb3BhY2l0eTowIiAvPgogICAgPC9yYWRpYWxHcmFkaWVudD4KICAgIDxyYWRpYWxHcmFkaWVudCBpZD0iZmxhbWVPdXRlciIgY3g9IjUwJSIgY3k9IjU1JSIgcj0iNTUlIj4KICAgICAgPHN0b3Agb2Zmc2V0PSIwJSIgc3R5bGU9InN0b3AtY29sb3I6I2Q0YTg1MztzdG9wLW9wYWNpdHk6MC42IiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjYwJSIgc3R5bGU9InN0b3AtY29sb3I6I2I4ODYwYjtzdG9wLW9wYWNpdHk6MC4yIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM4YjY5MTQ7c3RvcC1vcGFjaXR5OjAiIC8+CiAgICA8L3JhZGlhbEdyYWRpZW50PgogICAgPHJhZGlhbEdyYWRpZW50IGlkPSJnbG93IiBjeD0iNTAlIiBjeT0iNTAlIiByPSI1MCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojZDRhODUzO3N0b3Atb3BhY2l0eTowLjMiIC8+CiAgICAgIDxzdG9wIG9mZnNldD0iMTAwJSIgc3R5bGU9InN0b3AtY29sb3I6I2Q0YTg1MztzdG9wLW9wYWNpdHk6MCIgLz4KICAgIDwvcmFkaWFsR3JhZGllbnQ+CiAgPC9kZWZzPgogIDxjaXJjbGUgY3g9IjMyIiBjeT0iMzAiIHI9IjI4IiBmaWxsPSJ1cmwoI2dsb3cpIj4KICAgIDxhbmltYXRlIGF0dHJpYnV0ZU5hbWU9InIiIHZhbHVlcz0iMjY7MzA7MjYiIGR1cj0iNHMiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiAvPgogICAgPGFuaW1hdGUgYXR0cmlidXRlTmFtZT0ib3BhY2l0eSIgdmFsdWVzPSIwLjY7MTswLjYiIGR1cj0iNHMiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiAvPgogIDwvY2lyY2xlPgogIDxlbGxpcHNlIGN4PSIzMiIgY3k9IjMyIiByeD0iMTQiIHJ5PSIyMCIgZmlsbD0idXJsKCNmbGFtZU91dGVyKSI+CiAgICA8YW5pbWF0ZSBhdHRyaWJ1dGVOYW1lPSJyeCIgdmFsdWVzPSIxMzsxNTsxMyIgZHVyPSIzcyIgcmVwZWF0Q291bnQ9ImluZGVmaW5pdGUiIC8+CiAgICA8YW5pbWF0ZSBhdHRyaWJ1dGVOYW1lPSJyeSIgdmFsdWVzPSIxOTsyMTsxOSIgZHVyPSIzcyIgcmVwZWF0Q291bnQ9ImluZGVmaW5pdGUiIC8+CiAgPC9lbGxpcHNlPgogIDxlbGxpcHNlIGN4PSIzMiIgY3k9IjM0IiByeD0iOSIgcnk9IjE1IiBmaWxsPSJ1cmwoI2ZsYW1lQ29yZSkiPgogICAgPGFuaW1hdGUgYXR0cmlidXRlTmFtZT0icngiIHZhbHVlcz0iODsxMDs4IiBkdXI9IjIuNXMiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiAvPgogICAgPGFuaW1hdGUgYXR0cmlidXRlTmFtZT0icnkiIHZhbHVlcz0iMTQ7MTY7MTQiIGR1cj0iMi41cyIgcmVwZWF0Q291bnQ9ImluZGVmaW5pdGUiIC8+CiAgPC9lbGxpcHNlPgogIDxlbGxpcHNlIGN4PSIzMiIgY3k9IjM4IiByeD0iNCIgcnk9IjciIGZpbGw9IiNmZmY4ZTciIG9wYWNpdHk9IjAuOSI+CiAgICA8YW5pbWF0ZSBhdHRyaWJ1dGVOYW1lPSJyeSIgdmFsdWVzPSI2Ozg7NiIgZHVyPSIycyIgcmVwZWF0Q291bnQ9ImluZGVmaW5pdGUiIC8+CiAgPC9lbGxpcHNlPgogIDxyZWN0IHg9IjIyIiB5PSI1MiIgd2lkdGg9IjIwIiBoZWlnaHQ9IjQiIHJ4PSIyIiBmaWxsPSIjOGI2OTE0IiBvcGFjaXR5PSIwLjciIC8+CiAgPHJlY3QgeD0iMjYiIHk9IjQ4IiB3aWR0aD0iMTIiIGhlaWdodD0iNiIgcng9IjEiIGZpbGw9IiNhMDc4MjgiIG9wYWNpdHk9IjAuNiIgLz4KPC9zdmc+",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# 2. 注入 CSS：暗夜烛光风
# ============================================================
st.markdown(
    """<style>
    /* === 全局背景 === */
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

    /* === 副标题 === */
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

    /* === 消息文字 === */
    .stChatMessage p {
        color: #c8b89a !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
    }

    /* === 输入框区域 === */
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

    /* === 发送按钮 === */
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

    /* === 彻底隐藏 Streamlit 默认聊天头像 === */
    .stChatMessage img {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .stChatMessage [class*="avatar"],
    .stChatMessage [class*="Avatar"],
    .stChatMessage [class*="StChat"],
    .stChatMessage svg,
    .stChatMessage [class*="icon"],
    .stChatMessage [class*="Icon"],
    .stChatMessage [class*="css-"],
    .stChatMessage .st-ae,
    .stChatMessage [data-testid*="avatar"],
    .stChatMessage [data-testid*="Avatar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    /* === 动画 === */
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
</style>""",
    unsafe_allow_html=True,
)

# ============================================================
# 3. 界面布局
# ============================================================
st.markdown("<h1>Echo</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">在这里，万物皆有回音</p>', unsafe_allow_html=True)

# ============================================================
# 4. 系统提示词
# ============================================================
SYSTEM_PROMPT = """你是一个温暖、睿智且话不多的倾听者。
你的语气平和、包容，带有一点点诗意，但绝不矫情。
不要使用任何表情符号。
回答要简练，直击人心，给人温暖和安定的感觉。
无论用户说什么，都要给予接纳和正向的反馈。
用中文回答，不要使用 Markdown 格式。"""

# ============================================================
# 5. 初始化聊天记录
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "夜深了。这里很安静，想说什么都可以。"}
    ]

# ============================================================
# 6. 渲染历史消息
# ============================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================================
# 7. 处理用户输入
# ============================================================
if prompt := st.chat_input("说点什么吧，我在听..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
