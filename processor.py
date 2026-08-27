import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment or .env file!")

groq_client = Groq(api_key=api_key)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""]
)

def process_pdf(file_bytes: bytes, filename: str):

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    chunks=[]
    metadatas=[]
    ids=[]

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")

        if not text.strip():
            continue 

        page_chunks = text_splitter.split_text(text)

        for i,chunk in enumerate(page_chunks):
            chunks.append(chunk)

            metadatas.append({
                "source": filename,
                "page": page_num + 1
            })

            ids.append(f"{filename}_page{page_num+1}_chunk{i}")

    return chunks,metadatas,ids

def generate_answer(user_question: str, retrieved_chunks: list[str]):
    context_text = "\n\n---\n\n".join(retrieved_chunks)
    
    system_prompt = f"""
    You are an expert AI Study Assistant. Your goal is to help a student understand their college notes.
    Answer the user's question using ONLY the context provided below. 
    If the answer cannot be found in the context, respond strictly with: 
    "I cannot answer this based on the provided notes." Do NOT use your outside knowledge to fill in the gaps.
    Context: {context_text}

    Format your response clearly using bullet points, headings, or tables where appropriate to help the student learn.
    """

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        temperature=0.3,
        max_completion_tokens=1024
    )

    return response.choices[0].message.content
    