from fastapi import FastAPI
from app.api.routes import router  # Importing the API router with defined endpoints

# Initialize the FastAPI application
app = FastAPI()

# Include the API routes from the router (handles /upload and /ask)
app.include_router(router)

@app.get("/")
def root():
    """
    Root endpoint to verify that the backend is running.
    
    Returns:
    - A simple JSON message indicating the service status.
    """
    return {"message": "Wasserstoff Chatbot Backend Running"}