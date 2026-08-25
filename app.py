"""
AI Notes Assistant — Streamlit Frontend
========================================
A chat-based UI for querying uploaded PDF notes via a RAG pipeline.
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
    /* ── Source citation pills ──────────────── */
    .source-pill {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff !important;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 4px 5px 4px 0;
        font-weight: 500;
    }
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
    st.header("📚 AI Notes Assistant")
    st.caption("Upload your college notes and ask questions — powered by AI.")
    
    # Added a reset button so users can easily wipe the conversation
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.divider()

    # Enabled accept_multiple_files to allow batch uploading (up to your 10 doc cap)
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        help="Drag and drop or browse for your PDF files",
    )

    # Loop through the list of uploaded files
    if uploaded_files:
        for file in uploaded_files:
            # Only process if we haven't already uploaded it this session
            if file.name not in st.session_state.uploaded_files:
                with st.spinner(f"Processing {file.name}..."):
                    try:
                        files = {
                            "file": (
                                file.name,
                                file.getvalue(),
                                "application/pdf",
                            )
                        }
                        data = {"session_id": st.session_state.session_id}
                        
                        # Send file to backend
                        response = requests.post(
                            f"{BACKEND_URL}/upload", files=files, data=data, timeout=120
                        )

                        if response.status_code == 200:
                            result = response.json()
                            chunks = result.get("chunks_created", "?")
                            st.success(f"Indexed {file.name} ({chunks} chunks)")
                            st.session_state.uploaded_files.append(file.name)
                        else:
                            detail = response.json().get("detail", "Unknown error")
                            st.error(f"Upload failed for {file.name}: {detail}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot reach backend. Start FastAPI server.")
                    except Exception as e:
                        st.error(f"Error processing {file.name}: {e}")

    # Display list of successfully uploaded files
    if st.session_state.uploaded_files:
        st.divider()
        st.subheader("📁 Uploaded Files")
        for fname in st.session_state.uploaded_files:
            st.markdown(f"- {fname}")

    st.divider()
    st.caption(f"Session: `{st.session_state.session_id[:8]}...`")

# ──────────────────────────────────────────────
# Main Chat Area
# ──────────────────────────────────────────────
st.title("💬 Ask Your Notes")
st.caption("Upload PDFs in the sidebar, then ask anything about them here.")

# Render existing chat history
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])
        if entry["role"] == "assistant" and entry.get("sources"):
            source_html = "".join(
                f'<span class="source-pill">{s}</span>' for s in entry["sources"]
            )
            st.markdown(source_html, unsafe_allow_html=True)

# Chat input
user_question = st.chat_input("Ask a question about your notes...")

if user_question:
    # 1. Append and render user question
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # 2. Fetch and render assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "session_id": st.session_state.session_id,
                    "question": user_question,
                }
                resp = requests.post(
                    f"{BACKEND_URL}/query", json=payload, timeout=60
                )

                if resp.status_code == 200:
                    data = resp.json()
                    answer = data.get("answer", "No answer returned.")
                    sources = data.get("sources", [])

                    st.markdown(answer)

                    # Render sources as neat pills
                    if sources:
                        source_html = "".join(
                            f'<span class="source-pill">{s}</span>'
                            for s in sources
                        )
                        st.markdown(source_html, unsafe_allow_html=True)

                    # Save to state
                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        }
                    )
                else:
                    detail = resp.json().get("detail", "Backend error.")
                    st.error(detail)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": f"Error: {detail}", "sources": []}
                    )
            except requests.exceptions.ConnectionError:
                msg = "Backend is not reachable. Start the FastAPI server first."
                st.error(msg)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": msg, "sources": []}
                )
            except Exception as e:
                msg = f"Error: {e}"
                st.error(msg)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": msg, "sources": []}
                )