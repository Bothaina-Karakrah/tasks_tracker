"""
Runt the project using `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.routers import tasks, analytics, categories

# ---------- Logging Configuration ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- FastAPI App ----------
app = FastAPI(title="Task Management System", version="1.0.0")

# ---------- CORS Configuration ----------
# CORS middleware - MUST be added before other routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your exact domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ---------- Include API routers ----------
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

# ---------- Serve frontend static files ----------
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# ---------- Serve index.html at root ----------
@app.get("/", response_class=HTMLResponse)
def serve_index():
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        logger.error(f"Failed to load index.html: {e}")
        return HTMLResponse(content="Index file not found", status_code=404)