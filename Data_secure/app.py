import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# 🎨 
def inject_style():
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #e1bee7, #ce93d8, #b39ddb);
            color: #000000;
            font-family: 'Segoe UI', sans-serif;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #e1bee7, #ce93d8, #b39ddb);
            border-radius: 0px 20px 20px 0px;
            color: black;
        }

        section[data-testid="stSidebar"] label {
            font-size: 18px;
            font-weight: bold;
            color: #4A148C;
            margin-bottom: 8px;
            display: block;
            padding: 6px 12px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        section[data-testid="stSidebar"] label:hover {
            background-color: rgba(255,255,255,0.3);
            box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
            transform: scale(1.02);
        }

        h1 {
            color: #6A1B9A;
            font-size: 3rem;
            text-shadow: 2px 2px 5px yellow;
        }

        h2, h3 {
            color: #6A1B9A;
            font-family: 'Lucida Handwriting', cursive;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        }

        .stTextInput > div, .stTextArea > div, .stButton > button, .stCodeBlock, .stAlert {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-radius: 10px !important;
        }

        button[kind="primary"] {
            background: linear-gradient(to right, #ab47bc, #8e24aa, #b39ddb) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: bold;
            padding: 0.5rem 1.2rem !important;
            transition: all 0.3s ease;
        }

        button[kind="primary"]:hover {
            transform: scale(1.05);
            background: linear-gradient(to right, #b39ddb, #8e24aa, #ab47bc) !important;
        }

        pre {
            background-color: #f3e5f5 !important;
            color: #4a148c !important;
            border-radius: 10px;
        }

        /* 🦄 Footer */
        .footer-text {
            position: fixed;
            bottom: 10px;
            width: 100%;
            text-align: center;
            font-family: 'Brush Script MT', cursive;
            font-size: 1.5rem;
            color: #4A148C;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            background: rgba(255,255,255,0.1);
            padding: 8px;
            border-radius: 15px;
        }
        </style>
    """, unsafe_allow_html=True)



# 🔒 
if "vault" not in st.session_state: st.session_state.vault = {}
if "tries" not in st.session_state: st.session_state.tries = 0
if "lockout" not in st.session_state: st.session_state.lockout = False
if "fernet" not in st.session_state: st.session_state.fernet = Fernet(Fernet.generate_key())

# 🚀 
def hash(p): return hashlib.sha256(p.encode()).hexdigest()
def lock(t): return st.session_state.fernet.encrypt(t.encode()).decode()
def unlock(t): return st.session_state.fernet.decrypt(t.encode()).decode()

def auth_screen():
    st.title("🔐 Re-Login")
    u = st.text_input("👤 Username")
    p = st.text_input("🔑 Password", type="password")
    if st.button("Login"):
        if u == "admin" and p == "1234":
            st.success("✅ Access Restored.")
            st.session_state.tries = 0
            st.session_state.lockout = False
        else:
            st.error("❌ Invalid credentials.")

def save_page():
    st.title("➕ Save a Secret")
    k = st.text_input("📝 Label")
    msg = st.text_area("✍️ Secret Text")
    pwd = st.text_input("🔐 Passcode", type="password")
    if st.button("💾 Save"):
        if k and msg and pwd:
            st.session_state.vault[k] = {"text": lock(msg), "code": hash(pwd)}
            st.success("✅ Secret saved successfully!")
        else:
            st.warning("⚠️ Fill all fields.")

def access_page():
    if st.session_state.lockout:
        auth_screen()
        return
    st.title("🔓 Access a Secret")
    k = st.text_input("🆔 Label")
    pwd = st.text_input("🔐 Passcode", type="password")
    if st.button("🔍 Unlock"):
        data = st.session_state.vault.get(k)
        if data and hash(pwd) == data["code"]:
            st.success("🔓 Access Granted")
            st.code(unlock(data["text"]))
            st.session_state.tries = 0
        else:
            st.session_state.tries += 1
            st.error("❌ Wrong credentials!")
            if st.session_state.tries >= 3:
                st.warning("🚫 Locked. Re-auth required.")
                st.session_state.lockout = True

# 🎨 
inject_style()

# 📋
st.sidebar.title("⚙️ Menu")
choice = st.sidebar.radio("📂 Go to", [
    "🏠 Home",
    "➕ Save",
    "🔓 Access"
])

if choice == "🏠 Home":
    st.markdown("""
        <h1 style='text-align: center; color: #4A148C; font-size: 4rem; font-family: "Segoe UI", sans-serif;'>
            🔒 Secure Note Vault
        </h1>
        <h3 style='text-align: center; color: #6A1B9A; font-family: "Segoe UI", sans-serif;'>
            ✨ Keep your secrets safe and beautiful
        </h3>
        <div style='text-align: center; color: #4A148C; font-size: 1.4rem; font-family: "Segoe UI", sans-serif; margin-top: 30px;'>
            🔐 Encrypted in memory
        </div>
        <div style='text-align: center; color: #4A148C; font-size: 1.4rem; font-family: "Segoe UI", sans-serif;'>
            🧠 Lockout protection after 3 attempts
        </div>
        <div style='text-align: center; color: #4A148C; font-size: 1.4rem; font-family: "Segoe UI", sans-serif;'>
            ⚡ Fast, secure, and private
        </div>
    """, unsafe_allow_html=True)

elif choice == "➕ Save":
    save_page()
elif choice == "🔓 Access":
    access_page()
st.markdown("<div class='footer-text'>👑 Made by Moin Sheikh</div>", unsafe_allow_html=True)
