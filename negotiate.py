
import streamlit as st
import requests
import json
import re

# 初始化session state
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "deal_confirmed" not in st.session_state:
    st.session_state.deal_confirmed = False
if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False
if "debug_info" not in st.session_state:
    st.session_state.debug_info = []
if "deal_price" not in st.session_state:
    st.session_state.deal_price = None
if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# 配置信息
API_KEY = '9cef838868189adc'
API_SECRET = 'd17c0ea0a56cd28341d2d3de8e19079d'
ASSISTANT_ID = '68a69f039e5f1346214c52fb'
# 添加调试信息到session state
def add_debug_info(info):
    st.session_state.debug_info.append(info)
    if len(st.session_state.debug_info) > 20:
        st.session_state.debug_info.pop(0)

# 获取 Access Token（只执行一次）
def get_access_token(api_key, api_secret):
    url = "https://chatglm.cn/chatglm/assistant-api/v1/get_token"
    data = {"api_key": api_key, "api_secret": api_secret}

    try:
        response = requests.post(url, json=data, timeout=10)
        add_debug_info(f"Token状态: {response.status_code}")

        if response.status_code == 200:
            token_info = response.json()
            return token_info['result']['access_token']
        else:
            raise Exception(f"状态码: {response.status_code}")
    except Exception as e:
        raise Exception(f"Token获取失败: {str(e)}")

# 提取成交价格（优化版）
def extract_deal_price(text):
    # 优先匹配明确的成交价表达
    成交价模式 = [
        r'[成|交][价|格][是|为]?\s*(\d+(?:\.\d+)?)',
        r'以\s*(\d+(?:\.\d+)?)\s*元?[成|交]',
        r'(\d+(?:\.\d+)?)\s*元?[成|交][了|啦]?',
        r'最终[价|格][是|为]?\s*(\d+(?:\.\d+)?)',
        r'确定[价|格][是|为]?\s*(\d+(?:\.\d+)?)'
    ]
    
    for pattern in 成交价模式:
        match = re.search(pattern, text)
        if match:
            price = match.group(1)
            add_debug_info(f"提取到成交价: {price} (模式: {pattern})")
            return price
    
    # 如果没有明确成交价，匹配普通价格（但优先级较低）
    普通价格模式 = [
        r'(\d+(?:\.\d+)?)\s*元',
        r'(\d+(?:\.\d+)?)\s*块'
    ]
    
    for pattern in 普通价格模式:
        match = re.search(pattern, text)
        if match:
            price = match.group(1)
            add_debug_info(f"提取到普通价格: {price} (模式: {pattern})")
            return price
            
    return None

# 检查是否达成交易
def check_deal_confirmation(text):
    deal_keywords = ["成交", "接受", "可以交易", "同意", "成交价", "最终价格", "就这个价", "可以了", "就这样吧"]
    found_keywords = [keyword for keyword in deal_keywords if keyword in text]
    if found_keywords:
        add_debug_info(f"检测到成交关键词: {found_keywords}")
        return True
    return False

# 发送消息（使用流式请求获取完整响应）
def send_message(assistant_id, access_token, prompt):
    url = "https://chatglm.cn/chatglm/assistant-api/v1/stream"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "assistant_id": assistant_id,
        "prompt": prompt,
        "stream": True
    }

    try:
        add_debug_info(f"发送消息: {prompt[:50]}...")
        response = requests.post(url, json=data, headers=headers, timeout=30, stream=True)

        add_debug_info(f"响应状态: {response.status_code}")

        if response.status_code == 200:
            messages = []
            
            # 收集所有消息
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    line_str = line.decode('utf-8') if isinstance(line, bytes) else line
                    
                    # 检查是否是data行
                    if line_str.startswith('data:'):
                        json_str = line_str[5:].strip()  # 去掉"data:"前缀
                        if json_str == "[DONE]":
                            break
                            
                        try:
                            json_data = json.loads(json_str)
                            messages.append(json_data)
                        except json.JSONDecodeError:
                            continue
            
            add_debug_info(f"收到 {len(messages)} 条消息")
            
            # 只取最后一条消息的文本内容
            if messages:
                last_message = messages[-1]
                message = last_message.get("message", {})
                if message:
                    content = message.get("content", {})
                    if content.get("type") == "text":
                        text = content.get("text", "")
                        if text:
                            add_debug_info(f"提取到最后一条文本，长度: {len(text)}")
                            return text
            
            return "未获取到有效回复"
        else:
            return f"❌ 请求失败({response.status_code})"

    except Exception as e:
        add_debug_info(f"错误详情: {str(e)}")
        return f"❌ 错误：{str(e)}"

# 获取access token
if st.session_state.access_token is None:
    try:
        st.session_state.access_token = get_access_token(API_KEY, API_SECRET)
        add_debug_info("✅ Token获取成功")
    except Exception as e:
        st.error(f"❌ 无法获取 Access Token：{str(e)}")
        st.stop()

# 页面标题
st.title("🛍 【清仓竞价客服】VERO MODA")

# 商品展示区
try:
    st.image("https://img.alicdn.com/i1/420567757/O1CN01CyarLU27Al6HqCUCU_!!420567757.jpg", width=300)
except:
    pass

st.markdown("""
### 👗 商品名称：VERO MODA黄色连衣裙  
- 清仓价：¥350  
- 清仓特价：可议价  
""")

st.markdown("---")
st.markdown("### 💬 与客服机器人谈价")

# 显示聊天记录
for i, (role, msg) in enumerate(st.session_state.chat_history):
    st.chat_message(role).markdown(msg)
    
    # 检查是否达成交易
    if role == "assistant" and check_deal_confirmation(msg) and not st.session_state.deal_confirmed:
        price = extract_deal_price(msg)
        if price:
            st.session_state.deal_price = price
            st.success(f"🎉 恭喜您成功砍价！成交价：¥{st.session_state.deal_price}")
            if st.button("立即购买", key=f"buy_button_{i}"):
                st.session_state.deal_confirmed = True
                st.success("✅ 购买成功！感谢您的惠顾。")
                st.balloons()
        else:
            # 如果没提取到价格，显示默认信息
            st.success("🎉 恭喜您成功砍价！")
            if st.button("立即购买", key=f"buy_button_{i}"):
                st.session_state.deal_confirmed = True
                st.success("✅ 购买成功！感谢您的惠顾。")
                st.balloons()

# 如果已经成交但没有显示按钮，则显示
if st.session_state.deal_confirmed and st.session_state.deal_price:
    st.success(f"✅ 购买已完成！成交价：¥{st.session_state.deal_price}")
    st.balloons()

# 显示等待状态
if st.session_state.waiting_for_response:
    st.info("⏳ 正在等待客服回复，请稍候...")

# 用户输入和处理逻辑
user_input = st.chat_input("请输入您的出价或想法，例如：我出280元可以吗？", 
                           disabled=st.session_state.waiting_for_response,
                           key=f"chat_input_{st.session_state.message_count}")

if user_input and not st.session_state.waiting_for_response:
    # 添加用户消息到历史
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.waiting_for_response = True
    st.session_state.message_count += 1
    st.rerun()

# 处理AI响应
if st.session_state.waiting_for_response:
    with st.spinner("🤖 客服正在思考中..."):
        # 获取最新的用户消息
        last_user_message = st.session_state.chat_history[-1][1]
        # 调用API获取完整响应
        reply = send_message(ASSISTANT_ID, st.session_state.access_token, last_user_message)
        # 添加AI响应到历史
        st.session_state.chat_history.append(("assistant", reply))
        # 重置等待状态
        st.session_state.waiting_for_response = False
    st.rerun()

# 历史对话记录展示
st.markdown("---")
with st.expander("📚 历史对话记录", expanded=False):
    if st.session_state.chat_history:
        for i, (role, msg) in enumerate(st.session_state.chat_history):
            if role == "user":
                st.markdown(f"**👤 您**: {msg}")
            else:
                st.markdown(f"**🤖 客服**: {msg}")
            st.markdown("---")
    else:
        st.info("暂无对话记录")

# # 调试信息区域
# if st.checkbox("🔍 查看调试信息"):
#     st.markdown("### 调试信息")
#     for info in reversed(st.session_state.debug_info):
#         st.code(info)

# 页脚
st.markdown("---")
st.caption("© 2025 清仓竞价系统 | Powered by 智谱清言 & Streamlit")
