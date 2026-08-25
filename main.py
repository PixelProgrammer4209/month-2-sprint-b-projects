from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import api

app = FastAPI(title="AI Notes Assistant Backend")

# Allow Streamlit (typically running on localhost:8501) to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, change this to ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the endpoints from api.py
app.include_router(api.router)

@app.get("/")
def health_check():
    return {"status": "Backend is running smoothly"}