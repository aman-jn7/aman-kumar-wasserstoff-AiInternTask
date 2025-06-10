import faiss  # Facebook AI Similarity Search for fast vector search
import numpy as np

# Define the dimension of the embedding vectors
embedding_dim = 768

# Initialize a FAISS index for L2 (Euclidean) distance
index = faiss.IndexFlatL2(embedding_dim)

documents = []

def fake_embed(text):
    """
    Generate a fake embedding for demonstration using a seeded random vector.
    Replace this with real embeddings from OpenAI, Gemini, etc. in production.
    """
    np.random.seed(abs(hash(text)) % (10 ** 8))  # Stable random seed based on hash
    return np.random.rand(embedding_dim).astype("float32")

def store_text(text: str, metadata: dict):
    """
    Store a text chunk along with its metadata in both FAISS and the document store.

    Args:
        text (str): The extracted or chunked text content.
        metadata (dict): Information like filename, page number, paragraph, etc.
    """
    vector = fake_embed(text)
    index.add(np.array([vector]))  # Add vector to FAISS index
    documents.append({
        "text": text,
        "meta": metadata  # Store metadata for citation and referencing
    })

def search(query, top_k=5):
    """
    Perform semantic search against the stored text chunks.

    Args:
        query (str): The natural language question/query.
        top_k (int): Number of top matching results to return.

    Returns:
        list: Top matching document chunks with their metadata.
    """
    q_vec = fake_embed(query)
    distances, indices = index.search(np.array([q_vec]), top_k)
    return [documents[i] for i in indices[0]]
