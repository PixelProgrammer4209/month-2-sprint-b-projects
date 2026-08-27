from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import processor
import database

router = APIRouter()

class QueryRequest(BaseModel):
    session_id: str
    question: str

@router.post("/upload")
async def upload_pdf(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        
    try:
        file_bytes = await file.read()
        chunks, metadatas, ids = processor.process_pdf(file_bytes, file.filename)
        success = database.add_documents_to_collection(session_id, chunks, metadatas, ids)
        
        if success:
            return {
                "message": f"Successfully processed {file.filename}", 
                "chunks_created": len(chunks)
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save vectors to ChromaDB.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/query")
async def query_notes(request: QueryRequest):
    try:
        results = database.query_session_collection(request.session_id, request.question)
        
        if not results or not results["documents"][0]:
            return {
                "answer": "No context found. Please upload your college notes first.", 
                "sources": []
            }
            
        retrieved_chunks = results["documents"][0]
        retrieved_metadata = results["metadatas"][0]
        
        answer = processor.generate_answer(request.question, retrieved_chunks)
        
        sources = []
        for meta in retrieved_metadata:
            source_info = f"{meta['source']} (Page {meta['page']})"
            if source_info not in sources:
                sources.append(source_info)
                
        return {
            "answer": answer,
            "sources": sources
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")