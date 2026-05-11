"""
AI Chatbot - Powered by Groq API
A production-ready ChatGPT-like assistant for Python, SQL, and coding help.
"""

import os
import streamlit as st
from groq import Groq

# Load API key - works both locally and on Streamlit Cloud
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

if not GROQ_API_KEY:
    st.error("API Key not found! Add GROQ_API_KEY to your secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CodeMind AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import fonts ── */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── CSS variables ── */
:root {
    --bg-primary:    #0d0f14;
    --bg-secondary:  #13161e;
    --bg-card:       #181c27;
    --bg-input:      #1e2333;
    --accent:        #7c6af7;
    --accent-soft:   #9d8fff;
    --accent-glow:   rgba(124,106,247,0.15);
    --user-bubble:   #1e2a45;
    --ai-bubble:     #161b26;
    --border:        rgba(255,255,255,0.07);
    --text-primary:  #e8eaf0;
    --text-muted:    #6b7280;
    --text-code:     #a5d6ff;
    --success:       #34d399;
    --warning:       #fbbf24;
    --danger:        #f87171;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1rem !important;
}

/* ── Sidebar logo ── */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.5rem 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.sidebar-logo .logo-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, var(--accent), #5b4fcf);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    box-shadow: 0 0 20px var(--accent-glow);
}
.sidebar-logo .logo-text {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    background: linear-gradient(135deg, var(--accent-soft), #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ── Sidebar buttons ── */
.stButton > button {
    width: 100%;
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 0.6rem 1rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
}
.stButton > button:hover {
    background: var(--accent-glow) !important;
    border-color: var(--accent) !important;
    transform: translateX(2px) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-size: 0.85rem !important;
}
.stSelectbox label {
    font-size: 0.75rem !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* ── Main chat area ── */
.main-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: var(--bg-primary);
}

/* ── Top bar ── */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2rem;
    border-bottom: 1px solid var(--border);
    background: var(--bg-secondary);
    position: sticky;
    top: 0;
    z-index: 100;
}
.top-bar-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-primary);
}
.model-badge {
    background: var(--accent-glow);
    border: 1px solid var(--accent);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.75rem;
    color: var(--accent-soft);
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}

/* ── Chat messages container ── */
.chat-container {
    flex: 1;
    overflow-y: auto;
    padding: 2rem;
    max-width: 860px;
    margin: 0 auto;
    width: 100%;
}

/* ── Message bubbles ── */
.message-wrapper {
    display: flex;
    gap: 14px;
    margin-bottom: 1.5rem;
    animation: fadeSlideIn 0.3s ease;
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.message-wrapper.user { flex-direction: row-reverse; }

.avatar {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
    margin-top: 4px;
}
.avatar.user-avatar {
    background: linear-gradient(135deg, #3b5bdb, #364fc7);
    box-shadow: 0 2px 12px rgba(59,91,219,0.3);
}
.avatar.ai-avatar {
    background: linear-gradient(135deg, var(--accent), #5b4fcf);
    box-shadow: 0 2px 12px var(--accent-glow);
}

.bubble {
    max-width: 78%;
    padding: 0.9rem 1.2rem;
    border-radius: 14px;
    font-size: 0.9rem;
    line-height: 1.7;
    word-break: break-word;
}
.bubble.user-bubble {
    background: var(--user-bubble);
    border: 1px solid rgba(59,91,219,0.25);
    border-top-right-radius: 4px;
}
.bubble.ai-bubble {
    background: var(--ai-bubble);
    border: 1px solid var(--border);
    border-top-left-radius: 4px;
}

/* ── Code blocks inside bubbles ── */
.bubble pre {
    background: #0a0c12 !important;
    border: 1px solid rgba(124,106,247,0.2) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    overflow-x: auto !important;
    margin: 0.75rem 0 !important;
    color: var(--text-code) !important;
    position: relative;
}
.bubble code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    background: rgba(124,106,247,0.12) !important;
    padding: 0.15rem 0.4rem !important;
    border-radius: 4px !important;
    color: var(--accent-soft) !important;
}

/* ── Timestamp ── */
.msg-time {
    font-size: 0.68rem;
    color: var(--text-muted);
    margin-top: 4px;
    padding: 0 4px;
}

/* ── Welcome screen ── */
.welcome-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 60vh;
    text-align: center;
    padding: 2rem;
}
.welcome-icon {
    width: 72px;
    height: 72px;
    background: linear-gradient(135deg, var(--accent), #5b4fcf);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    margin: 0 auto 1.5rem;
    box-shadow: 0 0 40px var(--accent-glow);
}
.welcome-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    background: linear-gradient(135deg, var(--text-primary), var(--accent-soft));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.welcome-subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    max-width: 440px;
    line-height: 1.6;
    margin-bottom: 2rem;
}
.chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    max-width: 600px;
}
.chip {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 0.45rem 1rem;
    font-size: 0.8rem;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.2s;
}
.chip:hover {
    border-color: var(--accent);
    color: var(--accent-soft);
    background: var(--accent-glow);
}

/* ── Input area ── */
.input-area {
    padding: 1.25rem 2rem;
    border-top: 1px solid var(--border);
    background: var(--bg-secondary);
    max-width: 860px;
    margin: 0 auto;
    width: 100%;
}

/* ── Streamlit chat input override ── */
[data-testid="stChatInput"] {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    background: transparent !important;
}

/* ── Token stats bar ── */
.stats-bar {
    display: flex;
    gap: 1.5rem;
    padding: 0.5rem 0;
    font-size: 0.72rem;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
}
.stat-item { display: flex; align-items: center; gap: 6px; }
.stat-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
}

/* ── Sidebar section headers ── */
.sidebar-section {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    font-weight: 600;
    margin: 1.2rem 0 0.6rem;
    padding-left: 0.25rem;
}

/* ── Spinner override ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ── Download button ── */
.stDownloadButton > button {
    background: var(--bg-card) !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    padding: 0.4rem 0.8rem !important;
}
.stDownloadButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent-soft) !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Constants ─────────────────────────────────────────────────────────────────
MODELS = {
    "Llama 3.3 70B (Recommended)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B (Fastest)":      "llama-3.1-8b-instant",
    "Mixtral 8x7B":                 "mixtral-8x7b-32768",
    "Gemma 2 9B":                   "gemma2-9b-it",
}

SYSTEM_PROMPT = """You are CodeMind AI — an expert programming assistant specializing in:
• Python development (beginner to advanced)
• SQL query writing & optimization
• Coding interview preparation (DSA, system design)
• Code debugging & code review
• Explaining CS concepts clearly
• Generating clean, well-commented sample programs

Your response style:
- Always format code with proper syntax highlighting using markdown fences (```python, ```sql, etc.)
- Give concise, accurate, beginner-friendly explanations
- For debugging: identify the bug → explain why it's wrong → show the fix
- For interview questions: provide the optimal approach with time/space complexity
- For SQL: write clean, well-formatted queries with brief explanations
- Use bullet points for steps, numbered lists for sequences
- Keep responses focused and avoid unnecessary verbosity
- If code is requested, always include it

You are helpful, precise, and educational."""

STARTER_PROMPTS = [
    "🐍  Explain Python decorators",
    "🗄️  Write a SQL JOIN example",
    "🔍  Debug my Python code",
    "📊  Explain Big O notation",
    "🎯  LeetCode Two Sum problem",
    "⚡  Python list comprehensions",
    "🔧  How to use try/except?",
    "📋  Write a REST API in Python",
]


# ── Session state initialization ──────────────────────────────────────────────
def init_session():
    defaults = {
        "messages":       [],
        "total_tokens":   0,
        "prompt_tokens":  0,
        "compl_tokens":   0,
        "chat_id":        datetime.now().strftime("%Y%m%d_%H%M%S"),
        "model_key":      list(MODELS.keys())[0],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ── Groq client ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)

client = get_client()


# ── Helper: format messages for API ───────────────────────────────────────────
def build_api_messages():
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in st.session_state.messages:
        msgs.append({"role": m["role"], "content": m["content"]})
    return msgs


# ── Helper: render a single chat bubble ───────────────────────────────────────
def render_bubble(role: str, content: str, ts: str = ""):
    if role == "user":
        st.markdown(f"""
        <div class="message-wrapper user">
            <div class="avatar user-avatar">👤</div>
            <div>
                <div class="bubble user-bubble">{content}</div>
                <div class="msg-time" style="text-align:right">{ts}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Use st.markdown so code blocks get proper syntax highlighting
        col1, col2 = st.columns([0.05, 0.95])
        with col1:
            st.markdown('<div class="avatar ai-avatar">🤖</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(
                f'<div style="background:var(--ai-bubble);border:1px solid var(--border);'
                f'border-radius:14px;border-top-left-radius:4px;padding:0.9rem 1.2rem;'
                f'font-size:0.9rem;line-height:1.7">',
                unsafe_allow_html=True,
            )
            st.markdown(content)
            st.markdown('</div>', unsafe_allow_html=True)
            if ts:
                st.markdown(f'<div class="msg-time">{ts}</div>', unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">🤖</div>
        <div class="logo-text">CodeMind AI</div>
    </div>
    """, unsafe_allow_html=True)

    # New chat
    if st.button("✦  New Chat", key="new_chat"):
        st.session_state.messages      = []
        st.session_state.total_tokens  = 0
        st.session_state.prompt_tokens = 0
        st.session_state.compl_tokens  = 0
        st.session_state.chat_id       = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.rerun()

    # Clear history
    if st.button("🗑  Clear History", key="clear"):
        st.session_state.messages      = []
        st.session_state.total_tokens  = 0
        st.session_state.prompt_tokens = 0
        st.session_state.compl_tokens  = 0
        st.rerun()

    st.markdown('<div class="sidebar-section">Model</div>', unsafe_allow_html=True)
    model_key = st.selectbox(
        "Select Model",
        list(MODELS.keys()),
        index=list(MODELS.keys()).index(st.session_state.model_key),
        label_visibility="collapsed",
        key="model_select",
    )
    st.session_state.model_key = model_key

    st.markdown('<div class="sidebar-section">Specializations</div>', unsafe_allow_html=True)
    for label in ["🐍 Python Help", "🗄️ SQL Queries", "🎯 Interview Prep",
                  "🔍 Debugging", "📖 Concept Explainer", "⚡ Code Generation"]:
        st.markdown(
            f'<div style="padding:0.35rem 0.5rem;font-size:0.8rem;'
            f'color:var(--text-muted)">{label}</div>',
            unsafe_allow_html=True,
        )

    # Download chat
    if st.session_state.messages:
        st.markdown('<div class="sidebar-section">Export</div>', unsafe_allow_html=True)
        chat_text = "\n\n".join(
            f"[{m['role'].upper()}] {m['timestamp']}\n{m['content']}"
            for m in st.session_state.messages
        )
        st.download_button(
            label="⬇  Download Chat",
            data=chat_text,
            file_name=f"codemind_chat_{st.session_state.chat_id}.txt",
            mime="text/plain",
        )

        # Also offer JSON
        chat_json = json.dumps(st.session_state.messages, indent=2)
        st.download_button(
            label="⬇  Export as JSON",
            data=chat_json,
            file_name=f"codemind_chat_{st.session_state.chat_id}.json",
            mime="application/json",
        )

    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.72rem;color:var(--text-muted);text-align:center">'
        'Powered by <span style="color:var(--accent-soft)">Groq</span> · '
        '<span style="color:var(--accent-soft)">CodeMind AI</span></div>',
        unsafe_allow_html=True,
    )


# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-bar">
    <div class="top-bar-title">💬 Chat</div>
    <div class="model-badge">{MODELS[model_key].split("/")[-1]}</div>
</div>
""", unsafe_allow_html=True)


# ── Check API key ─────────────────────────────────────────────────────────────
if not os.getenv("GROQ_API_KEY"):
    st.markdown("""
    <div style="max-width:600px;margin:3rem auto;background:var(--bg-card);
    border:1px solid var(--danger);border-radius:14px;padding:2rem;text-align:center">
        <div style="font-size:2rem;margin-bottom:1rem">🔑</div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem;
        margin-bottom:0.75rem">API Key Required</div>
        <div style="color:var(--text-muted);font-size:0.88rem;line-height:1.6;margin-bottom:1rem">
            Set your <code>GROQ_API_KEY</code> environment variable to start chatting.<br>
            Get a free key at <strong>console.groq.com</strong>
        </div>
        <div style="background:#0a0c12;border:1px solid var(--border);border-radius:8px;
        padding:0.75rem 1rem;font-family:'JetBrains Mono',monospace;font-size:0.8rem;
        color:var(--text-code);text-align:left">
            # .env file<br>GROQ_API_KEY=gsk_your_key_here
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── Main chat area ────────────────────────────────────────────────────────────
chat_area = st.container()

with chat_area:
    if not st.session_state.messages:
        # Welcome / empty state
        st.markdown("""
        <div class="welcome-screen">
            <div class="welcome-icon">🤖</div>
            <div class="welcome-title">CodeMind AI</div>
            <div class="welcome-subtitle">
                Your expert assistant for Python, SQL, debugging, and coding interviews.
                Ask anything — I'll give you clean, optimized answers.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Starter chips as buttons
        cols = st.columns(4)
        for i, prompt in enumerate(STARTER_PROMPTS):
            with cols[i % 4]:
                if st.button(prompt, key=f"chip_{i}"):
                    st.session_state.messages.append({
                        "role": "user",
                        "content": prompt.split("  ", 1)[-1],
                        "timestamp": datetime.now().strftime("%H:%M"),
                    })
                    st.rerun()
    else:
        # Render conversation
        for msg in st.session_state.messages:
            render_bubble(msg["role"], msg["content"], msg.get("timestamp", ""))

        # Token stats
        if st.session_state.total_tokens > 0:
            st.markdown(f"""
            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-dot"></div>
                    Prompt: {st.session_state.prompt_tokens:,} tokens
                </div>
                <div class="stat-item">
                    <div class="stat-dot" style="background:var(--success)"></div>
                    Response: {st.session_state.compl_tokens:,} tokens
                </div>
                <div class="stat-item">
                    <div class="stat-dot" style="background:var(--warning)"></div>
                    Total: {st.session_state.total_tokens:,} tokens
                </div>
            </div>
            """, unsafe_allow_html=True)


# ── Chat input ────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Ask about Python, SQL, algorithms, debugging…"):
    # Append user message
    ts = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role":      "user",
        "content":   user_input,
        "timestamp": ts,
    })

    # Call Groq API
    try:
        with st.spinner(""):
            response = client.chat.completions.create(
                model=MODELS[st.session_state.model_key],
                messages=build_api_messages(),
                temperature=0.7,
                max_tokens=2048,
                stream=False,
            )

        ai_text = response.choices[0].message.content

        # Update token counts
        usage = response.usage
        st.session_state.prompt_tokens  += usage.prompt_tokens
        st.session_state.compl_tokens   += usage.completion_tokens
        st.session_state.total_tokens   += usage.total_tokens

        # Append AI message
        st.session_state.messages.append({
            "role":      "assistant",
            "content":   ai_text,
            "timestamp": datetime.now().strftime("%H:%M"),
        })

    except Exception as e:
        err_msg = str(e)
        if "authentication" in err_msg.lower() or "api_key" in err_msg.lower():
            friendly = "❌ **Invalid API Key** — Please check your `GROQ_API_KEY`."
        elif "rate_limit" in err_msg.lower():
            friendly = "⚠️ **Rate limit reached** — Please wait a moment and try again."
        elif "model" in err_msg.lower():
            friendly = f"⚠️ **Model error** — Try switching to a different model. ({err_msg})"
        else:
            friendly = f"⚠️ **Error**: {err_msg}"

        st.session_state.messages.append({
            "role":      "assistant",
            "content":   friendly,
            "timestamp": datetime.now().strftime("%H:%M"),
        })

    st.rerun()