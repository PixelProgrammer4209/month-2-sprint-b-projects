# Month 02 Sprint B - Final Projects

## Overview

This is the submission repository for the Month 2 Sprint B final projects.

Build an AI-powered application of your choice using the skills you've learned throughout this sprint — **RAG, embeddings, vector databases, semantic search, LLM integration, FastAPI, and deployment**.

You can pick one of the suggested project ideas or come up with your own. The main requirement is that your project must demonstrate a working **RAG pipeline** where relevant information is retrieved from a knowledge base and provided to an LLM to generate the response.

Your project must have:

* A FastAPI backend
* A RAG pipeline
* An LLM integration
* A frontend of your choice
* A vector database or vector store
* A live deployment

---

## Submission Guidelines

### 1. Fork the Repository

Fork the repository:

https://github.com/mulearngectcr/month-2-sprint-b-projects

Click the **Fork** button at the top-right of the repository.

### 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/month-2-sprint-b-projects.git
cd month-2-sprint-b-projects
```

### 3. Create a Folder with Your Name

Use lowercase letters and hyphens — no spaces.

```text
month-2-sprint-b-projects/
└── john-doe/
    ├── backend.py
    ├── rag.py
    ├── frontend.py        (or index.html / App.jsx / app.py etc.)
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    └── README.md
```

> ⚠️ Place all your project files inside your named folder. Do not put them in the root of the repository.

Your project structure does not have to exactly match the example above. You may organize your files however you prefer as long as the required components are present.

---

### 4. Add a README Inside Your Folder

Your named folder must contain a `README.md` that includes:

```markdown
## Project Name

## What it does
A short description of your project and the problem it solves.

## Tech Stack
- Backend: FastAPI
- Frontend: Streamlit / React / HTML etc.
- LLM: Groq / OpenAI / Gemini / etc.
- Embeddings: <embedding model>
- Vector Store: ChromaDB / FAISS / etc.
- Other libraries used

## RAG Pipeline
Briefly explain:
1. How your data is collected or loaded
2. How documents are chunked
3. How embeddings are generated
4. How documents are stored
5. How relevant documents are retrieved
6. How the retrieved context is passed to the LLM

## Live URLs
- Frontend: https://your-frontend-url
- Backend: https://your-backend-url

## How to run locally
Steps to set up and run the project locally.

## Environment Variables
Refer to `.env.example` for required keys.
```

---

### 5. Commit and Push

```bash
git add .
git commit -m "Add submission - John Doe"
git push origin main
```

### 6. Open a Pull Request

1. Go to your fork on GitHub.
2. Click **Contribute → Open Pull Request**.
3. Set the PR title to:

```text
Submission - John Doe
```

4. Add the following to the PR description:

```text
Project: <your project name>
Frontend URL: https://your-frontend-url
Backend URL: https://your-backend-url
```

---

## What to Submit

| Component                      | Required            |
| ------------------------------ | ------------------- |
| FastAPI backend                | ✅ Yes               |
| RAG pipeline                   | ✅ Yes               |
| Embedding model                | ✅ Yes               |
| Vector store / vector database | ✅ Yes               |
| LLM integration                | ✅ Yes               |
| Frontend                       | ✅ Yes               |
| `requirements.txt`             | ✅ Yes               |
| `.gitignore`                   | ✅ Yes               |
| `.env.example`                 | ✅ Yes               |
| `README.md` inside your folder | ✅ Yes               |
| `.env`                         | ❌ Never commit this |

---

## RAG Requirements

Your project must implement an actual RAG pipeline.

At minimum, your application should demonstrate:

```text
User Query
    ↓
Query Embedding
    ↓
Semantic Search
    ↓
Relevant Documents / Chunks
    ↓
Context + User Query
    ↓
LLM
    ↓
Generated Response
```

Simply sending the user's prompt directly to an LLM does **not** count as RAG.

The retrieved context should meaningfully influence the generated response.

---

## Project Ideas

You may build any RAG-based application. Some examples:

* **Study Assistant** — Upload notes or textbooks and ask questions about them.
* **Documentation Assistant** — Chat with a project's documentation.
* **College Knowledge Bot** — Search through college rules, notices, and resources.
* **Research Assistant** — Search and answer questions from a collection of papers or articles.
* **Resume Assistant** — Retrieve relevant information from a user's resume and generate tailored responses.
* **Legal Document Assistant** — Query a collection of provided legal documents.
* **Movie / Book Knowledge Bot** — Ask questions about a custom collection of books or movie data.
* **Personal Knowledge Base** — Store documents and interact with them through natural language.

You are encouraged to come up with your own idea rather than simply copying one of the examples.

---

## Deployment

Deploy your **FastAPI backend** to a platform such as:

* Render
* Railway
* Any other suitable cloud platform

Deploy your **frontend** to a platform such as:

* Streamlit Cloud
* Vercel
* Netlify
* GitHub Pages
* Any other suitable platform

Make sure your frontend calls your **deployed backend URL**, not `localhost`.

Your application must be publicly accessible and working at the time of submission.

Both the frontend and backend URLs must be included in your project's README and PR description.

---

## Important

* Do not commit API keys or other secrets.
* Use `.env` locally and provide a `.env.example` containing the required variable names.
* Do not put project files directly in the root of the repository.
* Your application must contain a functional RAG pipeline.
* The deployed application must be accessible without requiring the evaluator to run the project locally.
