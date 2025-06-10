import streamlit as st
import requests

st.title("Wasserstoff Gen-AI Chatbot")

# Section for uploading documents
st.subheader("Upload Documents")
uploaded_files = st.file_uploader(
    "Choose PDF files", 
    type=["pdf"], 
    accept_multiple_files=True
)

API_URL = "https://backend-iyoa.onrender.com"

# If files are uploaded by the user
if uploaded_files:
    with st.spinner("Uploading files..."):
        # Prepare files for POST request as multipart form data
        files = [("files", (f.name, f.read(), "application/pdf")) for f in uploaded_files]

        # Send POST request to backend API to upload and process files
        res = requests.post(f"{API_URL}/upload/", files=files)

        # Check if upload and processing was successful
        if res.status_code == 200:
            st.success("Documents processed!")
            # Display filename and preview content for each uploaded document
            for doc in res.json()["documents"]:
                st.markdown(f"**{doc.get('filename')}** preview:")
                st.code(doc.get("preview", ""), language="text")
        else:
            st.error("Upload failed")  # Show error if upload fails

# Section for user to ask questions
st.subheader("Ask a Question")
question = st.text_input("Enter your question")  # Input field for user's question

# When the user clicks the "Ask" button
if st.button("Ask"):
    with st.spinner("Fetching answer..."):
        # Send the user's question to the backend API
        res = requests.post(f"{API_URL}/ask/", params={"query": question})

        # If response is successful, display the answer
        if res.status_code == 200:
            st.markdown(res.json()["response"], unsafe_allow_html=True)
        else:
            st.error("Failed to get answer")  # Show error if question handling fails
