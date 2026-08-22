import streamlit as st
import base64
import os

# --- 1. 页面基础配置 (伪装成 APP) ---
st.set_page_config(
    page_title="ECHO",
    page_icon="🕯️",
    layout="wide",
    initial_sidebar_state="collapsed"  # 默认收起侧边栏
)

# --- 2. 强力 CSS 补丁 (核心修改：修复输入框不和谐 & 隐藏菜单) ---
hide_streamlit_style = """
<style>
    /* 隐藏顶部汉堡菜单和部署按钮 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* 隐藏右侧滚动条，让界面更像 APP */
    ::-webkit-scrollbar {display: none;}
    
    /* 全局字体和背景优化 */
    body {
        background-color: #0d0d0d; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 核心：把输入框区域改造成原生 APP 底部栏 */
    .stChatInputContainer {
        position: fixed !important;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 15px 20px 35px 20px; /* 底部留白适配 iPhone 底部横条 */
        background: linear-gradient(to top, #000000 80%, rgba(0,0,0,0)); /* 黑色渐变遮罩，防止文字穿帮 */
        z-index: 9999;
        border-top: 1px solid #1a1a1a;
    }
    
    /* 输入框本体样式 */
    .stChatInput {
        background-color: #1c1c1e !important;
        border: 1px solid #333 !important;
        border-radius: 24px !important;
        color: white !important;
        box-shadow: none !important;
    }
    
    /* 聊天记录区域的底部留白，防止被输入框挡住 */
    .block-container {
        padding-bottom: 100px !important; 
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 3. 处理图标 (兼容本地文件和 GitHub 环境) ---
def get_image_base64(image_path):
    """将图片转为 Base64 编码，防止网页加载失败"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return None

img_base64 = get_image_base64("echo_candle.svg")
img_tag = f'<img src="data:image/svg+xml;base64,{img_base64}" width="60" style="filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.6)); margin-bottom: 10px;">' if img_base64 else '🕯️'

# --- 4. 页面主体内容 ---
# 使用 flex 布局让内容垂直居中（模拟 APP 启动页）
st.markdown(f"""
<div style="height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
    <div style="font-size: 60px; margin-bottom: 10px;">{img_tag}</div>
    <h1 style="color: #e0e0e0; font-size: 3rem; letter-spacing: 5px; margin: 0;">ECHO</h1>
    <p style="color: #666; font-size: 1rem; margin-top: 10px;">在这里，万物皆有回音</p>
</div>
""", unsafe_allow_html=True)

# 模拟一句开场白
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "夜深了。这里很安静，想说什么都可以。"}]

# 渲染历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. 底部输入框逻辑 ---
if prompt := st.chat_input("说点什么吧，我在听..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()
