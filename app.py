import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccount.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://your-db.firebaseio.com"})

# Function to save messages to Firebase
def save_message(user, text):
    ref = db.reference("messages")
    ref.push({"user": user, "text": text})

# Function to fetch messages from Firebase
def fetch_messages():
    ref = db.reference("messages")
    return ref.get() or {}

# Streamlit UI Setup
st.set_page_config(page_title="Chat", layout="wide")

# Authentication
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

# User Selection
st.sidebar.title("👥 User Selection")
username = st.sidebar.radio("You are:", ["User 1", "User 2"])
st.sidebar.markdown("---")
st.sidebar.info("Password: `2331`")

# Chat Interface
st.title("📱 Chat")
chat_container = st.container()

# Display Previous Messages (From Firebase)
messages = fetch_messages()
for key, msg in messages.items():
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
        unsafe_allow_html=True,
    )

# Message Input Form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message", placeholder="Send a message...")
    submitted = st.form_submit_button("Send")
    if submitted and user_input.strip():
        save_message(username, user_input)
        st.rerun()
