import os
from dotenv import load_dotenv
import google.generativeai as genai
from app.core.faiss_db import search

# Load environment variables from .env file
load_dotenv()

# Fetch the Gemini API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API with the key
genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

def get_answer(query: str):
    """
    Given a user query, this function:
    - Retrieves the top 5 most relevant documents using a FAISS-based search.
    - Builds a markdown table of those documents with brief previews and citations.
    - Constructs a prompt including all relevant context.
    - Calls the Gemini model to generate a theme-based summary.
    - Returns the final markdown-formatted output.
    """

    # Search for relevant documents using the custom vector database
    docs = search(query, top_k=5)

    # Build a markdown table to preview individual document responses
    table = "| Document ID | Extracted Answer | Citation |\n"
    table += "|-------------|------------------|----------|\n"
    for i, doc in enumerate(docs):
        doc_id = f"DOC{str(i+1).zfill(3)}"  # Format: DOC001, DOC002, etc.
        answer_preview = doc["text"][:80].replace("\n", " ") + "..."  # Show first 80 chars as a preview
        citation = f"Page {doc['meta'].get('page', '-')}, Para {doc['meta'].get('paragraph', '-')}"
        table += f"| {doc_id} | {answer_preview} | {citation} |\n"

    # Concatenate the full text of retrieved documents for LLM context
    context = "\n\n".join([f"{doc['text']}" for doc in docs])

    # Construct a detailed prompt to guide the LLM in generating themed insights
    prompt = f"""
You're a legal document analyst.

Context:
{context}

Question:
{query}

Instructions:
- Summarize major themes across all documents.
- Label each theme and mention related DOC IDs.
- Explain each theme briefly.

Return the output in this format:
1. First a markdown table of individual document answers.
2. Then a section for Synthesized Theme Answer like:

Theme 1 - [Title]:
DOC001, DOC002: Explain here.

Theme 2 - ...
    """

    # Generate content from the Gemini model based on the prompt
    response = model.generate_content(prompt)

    # Combine the document answer table and the synthesized theme output
    final_output = f"### Document Answers\n\n{table}\n\n---\n\n### Synthesized Themes\n\n{response.text}"
    
    return final_output