import fitz  # PyMuPDF for reading and processing PDFs
import pytesseract  # Tesseract OCR for extracting text from images
import cv2  # OpenCV for image processing
import os
from app.core.faiss_db import store_text  # FAISS indexing utility

async def process_file(file):
    """
    Handles uploaded PDF file:
    - Extracts text using direct PDF parsing or OCR (if needed)
    - Stores extracted text with metadata (filename, page, paragraph) in FAISS
    - Returns a preview of extracted content for frontend display
    """
    contents = await file.read()

    # Create a temporary directory if not already exists
    os.makedirs("temp", exist_ok=True)

    # Save uploaded file to disk temporarily
    filepath = f"temp/{file.filename}"
    with open(filepath, "wb") as f:
        f.write(contents)

    all_text = ""       # To build the full extracted text
    all_chunks = []     # To collect individual page-wise chunks

    if file.filename.endswith('.pdf'):
        doc = fitz.open(filepath)

        # Loop through each page in the PDF
        for i, page in enumerate(doc):
            page_number = i + 1

            # Try to extract text directly from the PDF page
            text = page.get_text()

            # If the page has no text (i.e., it's a scanned image), use OCR
            if not text.strip():
                pix = page.get_pixmap()
                image_path = f"temp/page_{i}.png"
                pix.save(image_path)

                img = cv2.imread(image_path)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ocr_text = pytesseract.image_to_string(gray)
                text = ocr_text.strip()

                os.remove(image_path)  # Clean up temporary image

            # Store page-level chunk with metadata for citation
            chunk = {
                "text": text,
                "metadata": {
                    "filename": file.filename,
                    "page": page_number,
                    "paragraph": 1  # Assumption: One paragraph per page
                }
            }

            all_chunks.append(chunk)
            all_text += f"\nPage {page_number}:\n{text}"

        # Push all extracted chunks into FAISS vector store
        for chunk in all_chunks:
            store_text(chunk["text"], chunk["metadata"])

        # Prepare a short preview (first 10 lines) to send back to frontend
        preview = "\n".join(all_text.strip().splitlines()[:10])
        return {"filename": file.filename, "preview": preview}
    
    else:
        # If not a PDF file
        return {"error": "Unsupported format"}