# 🧠 Wasserstoff Gen-AI Document Research & Theme Identification Chatbot

A web-based chatbot application built as part of the Wasserstoff Gen-AI Internship Task.  
This system allows users to upload multiple documents (PDFs, scanned files), extract information, and get AI-generated answers and synthesized themes based on document content.

---

## 📁 Project Structure

chatbot_theme_identifier/
- ├── backend/
- │ ├── app/
- │ │ ├── api/ # FastAPI routes
- │ │ ├── core/ # FAISS vector search logic
- │ │ ├── services/ # OCR & LLM query handling
- │ │ └── main.py # FastAPI app entry point
- │ ├── .env # API keys (excluded from Git)
- │ └── requirements.txt
- ├── frontend/
- │ └── streamlit_app.py # Streamlit UI
- ├── README.md

## 🚀 Features

- ✅ Upload and process **multiple PDFs** (including scanned pages with OCR)
- ✅ Extract text using **Tesseract OCR** for image-based PDFs
- ✅ Store and index content using **FAISS vector store**
- ✅ Ask **natural language questions** about uploaded documents
- ✅ Get answers with:
  - 📄 Per-document citations (DocID, Page, Paragraph)
  - 💡 Synthesized theme-based summaries
- ✅ Clean and responsive frontend using **Streamlit**
- ✅ Powered by **Gemini 2.0 Flash**

---

## 🛠 Tech Stack

| Layer      | Technology            |
|------------|------------------------|
| LLM        | Gemini Pro / Flash     |
| OCR        | Tesseract + OpenCV     |
| Backend    | FastAPI (Python)       |
| Frontend   | Streamlit              |
| Vector DB  | FAISS                  |
| Deployment | Render (suggested)     |

---

## 📸 Sample Output Format

### Document Answers

| Document ID | Extracted Answer                  | Citation         |
|-------------|-----------------------------------|------------------|
| DOC001      | The order mentions a fine under..| Page 4, Para 2   |
| DOC002      | The tribunal cited disclosure... | Page 2, Para 1   |

---

### Synthesized Themes

**Theme 1 – Regulatory Non-Compliance**  
*DOC001, DOC002:* Highlight violations of SEBI Act and delay in disclosure.

**Theme 2 – Penalty Justification**  
*DOC001:* Discusses legal grounds for penalties.

---
