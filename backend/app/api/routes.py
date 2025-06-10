from typing import List
from fastapi import APIRouter, UploadFile, File, Query

# Import internal service functions
from app.services.ocr_processing import process_file
from app.services.query_handler import get_answer

# Initialize the FastAPI router to define API endpoints
router = APIRouter()

@router.post("/upload/")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Endpoint: POST /upload/
    
    Allows users to upload multiple PDF documents.
    Each document is processed using OCR or direct text extraction.
    Extracted content is stored in FAISS with citation metadata.
    
    Returns:
        A list of file summaries/previews with status.
    """
    results = []
    for file in files:
        result = await process_file(file)  # Process each file one by one
        results.append(result)
    return {"status": "processed", "documents": results}


@router.post("/ask/")
async def ask_question(query: str = Query(...)):
    """
    Endpoint: POST /ask/
    
    Accepts a natural language question.
    Performs semantic search over uploaded document embeddings.
    Sends results to Gemini to generate answer + theme-based synthesis.
    
    Returns:
        A formatted response string with document answers and themes.
    """
    response = get_answer(query)
    return {"response": response}
