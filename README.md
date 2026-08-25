# 📚 AI Notes Assistant

> **A Retrieval-Augmented Generation (RAG) application that lets students upload PDF notes and ask questions — powered by LLMs.**

Upload your lecture slides, textbook chapters, or study materials. The AI reads, indexes, and answers your questions using **only** the content you provide — no hallucinations, just your notes.

---

## 🏗️ System Architecture

```mermaid
graph TD
    A["👤 User"] -->|Uploads PDF / Asks Question| B["🖥️ Streamlit<br/>Frontend"]
    B -->|POST /upload<br/>(multipart/form-data)| C["⚡ FastAPI<br/>Backend Router"]
    B -->|POST /query<br/>(JSON)| C
    C -->|Extract text from PDF| D["📄 PyMuPDF<br/>Text Extractor"]
    D -->|Chunked text<br/>(1000 / 200 overlap)| E["🗄️ ChromaDB<br/>Vector Vault"]
    C -->|Retrieve relevant chunks| E
    E -->|Top-K context| F["🤖 Groq LLM<br/>Llama 3.3 70B"]
    F -->|Generated answer + sources| C
    C -->|JSON response| B
    B -->|Rendered answer| A

    style A fill:#667eea,stroke:#333,color:#fff
    style B fill:#f093fb,stroke:#333,color:#fff
    style C fill:#4facfe,stroke:#333,color:#fff
    style D fill:#43e97b,stroke:#333,color:#fff
    style E fill:#fa709a,stroke:#333,color:#fff
    style F fill:#fee140,stroke:#333,color:#333
```

---

## 🛠️ Tech Stack

| Layer        | Technology                          | Purpose                        |
| ------------ | ----------------------------------- | ------------------------------ |
| **Frontend** | Streamlit                           | Chat UI & file upload          |
| **Backend**  | FastAPI                             | REST API routing               |
| **PDF**      | PyMuPDF (fitz)                      | Text extraction from PDFs      |
| **Chunking** | LangChain `RecursiveCharacterTextSplitter` | Smart text splitting (1000/200) |
| **Vector DB**| ChromaDB                            | Embedding storage & retrieval  |
| **LLM**      | Groq (Llama 3.3 70B Versatile)      | Answer generation              |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A free [Groq API key](https://console.groq.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/PixelProgrammer4209/month-2-sprint-b-projects.git
cd month-2-sprint-b-projects
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY="your_groq_api_key_here"
```

### 5. Run the Application

Open **two terminals** (both with the virtual environment activated):

**Terminal 1 — Backend (FastAPI):**

```bash
uvicorn main:app --reload
```

The API will be live at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

**Terminal 2 — Frontend (Streamlit):**

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📖 Usage

1. **Upload** a PDF in the sidebar.
2. **Ask** any question about the uploaded content in the chat box.
3. **Review** the AI-generated answer along with source references (file name & page number).

---

## 📂 Project Structure

```
ai-notes-assistant/
├── main.py             # FastAPI application entry-point
├── api.py              # /upload and /query route handlers
├── processor.py        # PDF text extraction & LLM answer generation
├── database.py         # ChromaDB vector store operations
├── app.py              # Streamlit chat frontend
├── requirements.txt    # Python dependencies
├── .env                # API keys (git-ignored)
├── .gitignore          # Ignore rules
└── README.md           # This file
```

---

## 📝 License

This project is built for educational purposes as part of the **µLearn Month 2 Sprint B** program.

---

<p align="center">Built with ❤️ using FastAPI, Streamlit, ChromaDB & Groq</p>
