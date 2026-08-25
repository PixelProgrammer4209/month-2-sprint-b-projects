"""
AI Notes Assistant — Streamlit Frontend
========================================
A chat-based UI for querying uploaded PDF notes via a RAG pipeline.
Communicates with the FastAPI backend at http://localhost:8000.
"""

import streamlit as st
import requests
import uuid

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Notes Assistant",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

BACKEND_URL = "http://localhost:8000"

# ──────────────────────────────────────────────
# Custom Styling
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Global ─────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }

    /* ── Sidebar ────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

    /* ── Source pills ───────────────────────── */
    .source-pill {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        margin: 3px 4px 3px 0;
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    /* ── Chat bubbles ───────────────────────── */
    .stChatMessage { border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# Session State Initialisation
# ──────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# ──────────────────────────────────────────────
# Sidebar — File Upload
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 AI Notes Assistant")
    st.caption("Upload your college notes and ask questions powered by AI.")
    st.divider()

    st.markdown("### 📄 Upload Notes")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload a PDF of your lecture notes, textbook chapter, or study material.",
    )

    if uploaded_file is not None:
        # Prevent duplicate uploads of the same file in this session
        if uploaded_file.name not in st.session_state.uploaded_files:
            with st.spinner(f"Processing **{uploaded_file.name}**…"):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    data = {"session_id": st.session_state.session_id}
                    response = requests.post(f"{BACKEND_URL}/upload", files=files, data=data, timeout=120)

                    if response.status_code == 200:
                        result = response.json()
                        st.success(
                            f"✅ **{uploaded_file.name}** processed — "
                            f"{result.get('chunks_created', '?')} chunks indexed."
                        )
                        st.session_state.uploaded_files.append(uploaded_file.name)
                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.error(f"❌ Upload failed: {error_detail}")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Cannot reach the backend. Is `uvicorn main:app --reload` running on port 8000?")
                except Exception as e:
                    st.error(f"⚠️ Unexpected error: {e}")
        else:
            st.info(f"ℹ️ **{uploaded_file.name}** is already uploaded in this session.")

    # Show uploaded files list
    if st.session_state.uploaded_files:
        st.divider()
        st.markdown("### 🗂️ Uploaded Files")
        for fname in st.session_state.uploaded_files:
            st.markdown(f"- 📎 `{fname}`")

    st.divider()
    st.caption(f"🔑 Session: `{st.session_state.session_id[:8]}…`")

# ──────────────────────────────────────────────
# Main Chat Area
# ──────────────────────────────────────────────
st.markdown("# 💬 Ask Your Notes")
st.caption("Upload PDFs in the sidebar, then ask anything about them here.")

# Render chat history
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])

        # Re-render sources for assistant messages
        if entry["role"] == "assistant" and entry.get("sources"):
            source_html = "".join(
                f'<span class="source-pill">📄 {src}</span>' for src in entry["sources"]
            )
            st.markdown(
                f'<div style="margin-top:8px;">{source_html}</div>',
                unsafe_allow_html=True,
            )

# Chat input
user_question = st.chat_input("Ask a question about your notes…")

if user_question:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Query the backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                payload = {
                    "session_id": st.session_state.session_id,
                    "question": user_question,
                }
                resp = requests.post(f"{BACKEND_URL}/query", json=payload, timeout=60)

                if resp.status_code == 200:
                    data = resp.json()
                    answer = data.get("answer", "No answer returned.")
                    sources = data.get("sources", [])

                    st.markdown(answer)

                    # Render sources as styled pills
                    if sources:
                        source_html = "".join(
                            f'<span class="source-pill">📄 {src}</span>' for src in sources
                        )
                        st.markdown(
                            f'<div style="margin-top:8px;">{source_html}</div>',
                            unsafe_allow_html=True,
                        )

                    # Save to history
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer, "sources": sources}
                    )
                else:
                    error_msg = resp.json().get("detail", "Unknown backend error.")
                    st.error(f"❌ {error_msg}")
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": f"❌ Error: {error_msg}", "sources": []}
                    )

            except requests.exceptions.ConnectionError:
                err = "🔌 Backend is not reachable. Please start the FastAPI server."
                st.error(err)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": err, "sources": []}
                )
            except Exception as e:
                err = f"⚠️ Unexpected error: {e}"
                st.error(err)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": err, "sources": []}
                )
