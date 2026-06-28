import streamlit as st
import time
from chatbot import get_response, build_history
from intents import detect_intent, is_emergency, EMERGENCY_RESPONSE

st.set_page_config(page_title="MediAssist", page_icon="🩺", layout="wide", initial_sidebar_state="expanded")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "theme" not in st.session_state:
    st.session_state.theme = "dark"


theme_attr = 'data-theme="light"' if st.session_state.theme == "light" else 'data-theme="dark"'

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, html, body, [class*="css"] { 
    font-family: 'Inter', sans-serif !important; 
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── CONSTANT CENTERED LAYOUT (ChatGPT Style Column) ── */
[data-testid="stChatMessageContainer"], 
.welcome, 
.emergency-msg,
[data-testid="stChatInput"] { 
    max-width: 760px !important; 
    margin: 0 auto !important; 
}

/* Eliminate default Streamlit message containers & backgrounds */
[data-testid="stChatMessage"] { 
    background-color: transparent !important; 
    border: none !important; 
    padding: 1.5rem 0rem !important; 
    box-shadow: none !important;
}

/* Custom text styling within message streams */
[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] li { 
    font-size: 0.95rem !important; 
    line-height: 1.75 !important; 
}
[data-testid="stChatMessageContent"] strong { 
    font-weight: 600 !important; 
}

/* Sticky Input bar clean-up */
.stChatFloatingInputContainer { 
    background: transparent !important; 
    border-top: none !important; 
    padding: 10px 0 !important;
}

/* ── DARK THEME INJECTIONS ── */
[data-theme="dark"], .stApp {
    background-color: #0d0e12 !important;
}
[data-theme="dark"] [data-testid="stSidebar"] {
    background: #111217 !important;
    border-right: 1px solid #1e2026 !important;
}
[data-theme="dark"] [data-testid="stChatMessageContent"] p,
[data-theme="dark"] [data-testid="stChatMessageContent"] li {
    color: #e3e6ed !important;
}
[data-theme="dark"] [data-testid="stChatMessageContent"] strong {
    color: #ffffff !important;
}
[data-theme="dark"] [data-testid="stChatInputTextArea"] {
    background: #16181f !important;
    border: 1px solid #242831 !important;
    border-radius: 14px !important;
    color: #e3e6ed !important;
}
[data-theme="dark"] .chip {
    background: #16181f;
    border: 1px solid #242831;
    color: #8e95a5;
}

/* ── LIGHT THEME INJECTIONS ── */
[data-theme="light"], .stApp.light {
    background-color: #f9fafb !important;
}
[data-theme="light"] [data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e5e7eb !important;
}
[data-theme="light"] [data-testid="stChatMessageContent"] p,
[data-theme="light"] [data-testid="stChatMessageContent"] li {
    color: #1f2937 !important;
}
[data-theme="light"] [data-testid="stChatMessageContent"] strong {
    color: #111827 !important;
}
[data-theme="light"] [data-testid="stChatInputTextArea"] {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 14px !important;
    color: #1f2937 !important;
}
[data-theme="light"] .chip {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    color: #4b5563;
}

/* ── INTERFACE COMPONENTS ── */
.welcome { 
    display: flex; 
    flex-direction: column; 
    align-items: center; 
    justify-content: center; 
    padding-top: 15vh;
    gap: 12px; 
}
.welcome-heading { font-size: 2rem; font-weight: 700; text-align: center; margin-bottom: 4px; }
[data-theme="dark"] .welcome-heading { color: #ffffff; }
[data-theme="light"] .welcome-heading { color: #111827; }

.welcome-sub { font-size: 0.9rem; text-align: center; }
[data-theme="dark"] .welcome-sub { color: #6b7280; }
[data-theme="light"] .welcome-sub { color: #6b7280; }

.chips { display: flex; gap: 10px; margin-top: 24px; flex-wrap: wrap; justify-content: center; }
.chip { 
    padding: 10px 18px; 
    border-radius: 24px; 
    font-size: 0.82rem; 
    font-weight: 500;
    cursor: pointer;
}

.sidebar-title { font-size: 1.15rem; font-weight: 700; padding: 24px 4px 2px; }
[data-theme="dark"] .sidebar-title { color: #ffffff; }
[data-theme="light"] .sidebar-title { color: #111827; }

.sidebar-sub { font-size: 0.78rem; color: #6b7280; padding: 0 4px 18px; }
.sidebar-section { font-size: 0.72rem; font-weight: 600; color: #4b5563; text-transform: uppercase; letter-spacing: 0.05em; padding: 16px 4px 6px; }

.history-item { padding: 9px 12px; border-radius: 8px; font-size: 0.85rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 4px; }
[data-theme="dark"] .history-item { color: #9ca3af; }
[data-theme="light"] .history-item { color: #4b5563; }
[data-theme="dark"] .history-item.active { background: #1f2937; color: #ffffff; }
[data-theme="light"] .history-item.active { background: #e5e7eb; color: #111827; }

.sidebar-footer { font-size: 0.72rem; color: #9ca3af; line-height: 1.6; padding: 4px; margin-top: 30px; border-top: 1px solid rgba(128,128,128,0.1); padding-top: 12px; }
.disclaimer { text-align: center; font-size: 0.75rem; color: #6b7280; margin-top: 20px; padding-bottom: 12px; }

.emergency-msg { 
    background: #1a0b0b; 
    border: 1px solid #451a1a; 
    border-radius: 12px; 
    padding: 16px 20px; 
    color: #f87171; 
    font-size: 0.92rem; 
    line-height: 1.7; 
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f'<script>document.documentElement.setAttribute("data-theme", "{st.session_state.theme}")</script>', unsafe_allow_html=True)

def start_new_chat():
    if st.session_state.messages:
        st.session_state.chat_history.insert(0, st.session_state.messages.copy())
    st.session_state.messages = []

with st.sidebar:
    st.markdown('<div class="sidebar-title">MediAssist</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Your Personal Healthcare Assistant</div>', unsafe_allow_html=True)

    if st.button("+ New Chat", use_container_width=True, key="new_chat"):
        start_new_chat()
        st.rerun()

    theme_label = "Light Mode" if st.session_state.theme == "dark" else "Dark Mode"
    if st.button(theme_label, use_container_width=True, key="theme_toggle"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

    if st.session_state.messages or st.session_state.chat_history:
        st.markdown('<div class="sidebar-section">Recents</div>', unsafe_allow_html=True)
        if st.session_state.messages:
            label = st.session_state.messages[0]["content"]
            label = label[:35] + "..." if len(label) > 35 else label
            st.markdown(f'<div class="history-item active">{label}</div>', unsafe_allow_html=True)
        for past in st.session_state.chat_history[:5]:
            if past:
                label = past[0]["content"]
                label = label[:35] + "..." if len(label) > 35 else label
                st.markdown(f'<div class="history-item">{label}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-footer">MediAssist does not replace professional medical advice. Always consult a qualified healthcare provider.</div>', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown(f"""
    <div class="welcome">
        <div class="welcome-heading">How can I help you today?</div>
        <div class="welcome-sub">Ask about symptoms, medications, mental health, or first aid.</div>
        <div class="chips">
            <div class="chip">What are symptoms of diabetes?</div>
            <div class="chip">How to manage anxiety?</div>
            <div class="chip">What does ibuprofen treat?</div>
            <div class="chip">First aid for a burn?</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg.get("emergency"):
            st.markdown(f'<div class="emergency-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            with st.chat_message(msg["role"], avatar="🩺" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["content"])

if prompt := st.chat_input("Ask a health question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    if is_emergency(prompt):
        st.markdown(f'<div class="emergency-msg">{EMERGENCY_RESPONSE}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": EMERGENCY_RESPONSE, "emergency": True})
    else:
        with st.chat_message("assistant", avatar="🩺"):
            placeholder = st.empty()
            history = build_history(st.session_state.messages[:-1])
            history.append({"role": "user", "content": prompt})
            
            full_response = get_response(history)
            displayed = ""
        
            for char in full_response:
                displayed += char
                placeholder.markdown(displayed + "▌")
                time.sleep(0.005)
            placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.rerun()

st.markdown('<div class="disclaimer">MediAssist provides general information only. Not a substitute for professional medical advice.</div>', unsafe_allow_html=True)
