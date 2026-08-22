import streamlit as st
from openai import OpenAI

# --- 1. 页面配置：极简沉浸 ---
st.set_page_config(page_title="Echo", page_icon="🕯️", layout="centered", initial_sidebar_state="collapsed")

# --- 2. 注入风水 CSS：暗水暖阳 ---
st.markdown("""
<style>
    /* 全局背景：深邃暗色（藏水），带微弱的暖光 */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #2a1f24 0%, #0a0809 70%, #000000 100%);
        color: #dcdcdc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    /* 隐藏所有默认UI */
    #MainMenu, footer, header {visibility: hidden;}
    .stDecoration {display: none;}
    .block-container {padding-top: 3rem; padding-bottom: 2rem;}

    /* 标题：琥珀金，温暖而不刺眼 */
    h1 {
        color: #e8c382;
        text-align: center;
        font-family: 'Georgia', serif;
        text-shadow: 0 0 20px rgba(232, 195, 130, 0.2);
        margin-bottom: 0.5rem;
        font-weight: 400;
    }
    .subtitle {
        text-align: center;
        color: #8a7b70;
        font-style: italic;
        margin-bottom: 3rem;
        font-size: 0.9rem;
    }

    /* 聊天气泡：磨砂质感 */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(232, 195, 130, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }

    /* 输入框：微光呼吸感 */
    .stChatInput input {
        background-color: rgba(20, 15, 15, 0.8);
        color: #fff;
        border: 1px solid #4a3b32;
        border-radius: 30px !important;
        padding: 15px 25px;
        transition: all 0.3s ease;
    }
    .stChatInput input:focus {
        border-color: #e8c382 !important;
        box-shadow: 0 0 15px rgba(232, 195, 130, 0.15);
    }
    button[kind="primary"] {
        background-color: #4a3b32 !important;
        color: #e8c382 !important;
        border-radius: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 界面布局 ---
st.markdown("<h1>ECHO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>在这里，万物皆有回音</p>", unsafe_allow_html=True)

# --- 4. 对话逻辑 ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "晚上好。这里很安静，想说什么都可以。"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("说点什么吧，我在听..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            client = OpenAI(
                api_key=st.secrets["OPENAI_API_KEY"],
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            
            # 核心灵魂：隐藏的风水提示词
            system_prompt = """
            你是一个温暖、睿智且话不多的倾听者。
            你的语气平和、包容，带有一点点诗意，但绝不矫情。
            不要使用任何表情符号。
            回答要简练，直击人心，给人温暖和安定的感觉。
            无论用户说什么，都要给予接纳和正向的反馈。
            """
            
            stream = client.chat.completions.create(
                model="qwen-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages
                ],
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "🕯️") 
            placeholder.markdown(full_response)
            
        except Exception as e:
            placeholder.markdown("连接似乎断开了，请稍后再试...")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
