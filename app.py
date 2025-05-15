import streamlit as st
import time

# Set page config
st.set_page_config(page_title="Chat", layout="wide")

# Password protection
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Enter Chat Room")
    password = st.text_input("Enter Password", type="password")
    if password == "2331":
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.stop()

# Initialize chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# User selection
st.sidebar.title("👥 User Selection")
username = st.sidebar.radio("You are:", ["User 1", "User 2"])
st.sidebar.markdown("---")
st.sidebar.info("Password: `2331`")

# Chat interface
st.title("📱 Chat")
chat_container = st.container()

# Display previous messages
with chat_container:
    for msg in st.session_state.messages:
        is_user = msg["user"] == username
        align = "flex-end" if is_user else "flex-start"
        bg_color = "#cce5ff" if is_user else "#f1f1f1"
        st.markdown(
            f"""
            <div style="display: flex; justify-content: {align}; margin: 5px 0;">
                <div style="background-color: {bg_color}; padding: 10px 15px; border-radius: 10px; max-width: 60%;">
                    <strong>{msg['user']}</strong><br>{msg['text']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Message input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message", placeholder="Send a message...")
    submitted = st.form_submit_button("Send")
    if submitted and user_input.strip():
        st.session_state.messages.append({"user": username, "text": user_input})
        time.sleep(0.2)
        st.rerun()
