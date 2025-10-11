from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from datetime import datetime

from database import init_db, get_db, Podcast, Transcription, ChatSession, ChatMessage
from transcription_service import transcribe_audio
from chatbot_service import ChatbotService
from vector_store import VectorStore

app = FastAPI(title="Podcast Chatbot API")

# Initialize services
chatbot_service = ChatbotService()
vector_store = VectorStore()

# Create upload directory
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize database
init_db()


# Pydantic models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    session_id: int


class PodcastResponse(BaseModel):
    id: int
    title: str
    filename: str
    upload_date: datetime
    transcription_status: str


class TranscriptionResponse(BaseModel):
    id: int
    podcast_id: int
    full_text: str
    created_at: datetime


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime


# Background task for transcription
def process_transcription(podcast_id: int, file_path: str, db_session):
    """Background task to process podcast transcription"""
    from database import SessionLocal
    db = SessionLocal()

    try:
        # Update status to processing
        podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
        podcast.transcription_status = "processing"
        db.commit()

        # Transcribe audio
        result = transcribe_audio(file_path)

        # Save transcription
        transcription = Transcription(
            podcast_id=podcast_id,
            full_text=result["text"],
            duration=result.get("duration")
        )
        db.add(transcription)

        # Create vector store
        vector_store.create_collection_for_podcast(podcast_id, result["text"])

        # Update status to completed
        podcast.transcription_status = "completed"
        db.commit()

    except Exception as e:
        podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
        podcast.transcription_status = "failed"
        db.commit()
        print(f"Transcription failed: {str(e)}")
    finally:
        db.close()


# API Endpoints
@app.post("/api/podcasts/upload", response_model=PodcastResponse)
async def upload_podcast(
    background_tasks: BackgroundTasks,
    title: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a podcast audio file"""
    # Validate file type
    allowed_extensions = [".mp3", ".wav", ".m4a", ".mp4", ".mpeg", ".mpga", ".webm"]
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Save file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create database entry
    podcast = Podcast(
        title=title,
        filename=file.filename,
        file_path=file_path,
        transcription_status="pending"
    )
    db.add(podcast)
    db.commit()
    db.refresh(podcast)

    # Start transcription in background
    background_tasks.add_task(process_transcription, podcast.id, file_path, db)

    return podcast


@app.get("/api/podcasts", response_model=List[PodcastResponse])
def get_podcasts(db: Session = Depends(get_db)):
    """Get all podcasts"""
    podcasts = db.query(Podcast).order_by(Podcast.upload_date.desc()).all()
    return podcasts


@app.get("/api/podcasts/{podcast_id}", response_model=PodcastResponse)
def get_podcast(podcast_id: int, db: Session = Depends(get_db)):
    """Get a specific podcast"""
    podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    return podcast


@app.get("/api/podcasts/{podcast_id}/transcription", response_model=TranscriptionResponse)
def get_transcription(podcast_id: int, db: Session = Depends(get_db)):
    """Get transcription for a podcast"""
    transcription = db.query(Transcription).filter(
        Transcription.podcast_id == podcast_id
    ).first()

    if not transcription:
        raise HTTPException(status_code=404, detail="Transcription not found")

    return transcription


@app.post("/api/podcasts/{podcast_id}/chat", response_model=ChatResponse)
def chat_with_podcast(
    podcast_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Chat with a podcast using its transcription"""
    # Verify podcast exists and has transcription
    podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")

    if podcast.transcription_status != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Transcription not ready. Status: {podcast.transcription_status}"
        )

    # Get or create chat session
    if request.session_id:
        session = db.query(ChatSession).filter(ChatSession.id == request.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
    else:
        session = ChatSession(podcast_id=podcast_id)
        db.add(session)
        db.commit()
        db.refresh(session)

    # Get chat history
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).order_by(ChatMessage.timestamp).all()

    chat_history = [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]

    # Generate response
    response_text = chatbot_service.generate_response(
        podcast_id,
        request.message,
        chat_history
    )

    # Save messages
    user_message = ChatMessage(
        session_id=session.id,
        role="user",
        content=request.message
    )
    assistant_message = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=response_text
    )

    db.add(user_message)
    db.add(assistant_message)
    db.commit()

    return ChatResponse(response=response_text, session_id=session.id)


@app.get("/api/sessions/{session_id}/messages", response_model=List[MessageResponse])
def get_session_messages(session_id: int, db: Session = Depends(get_db)):
    """Get all messages from a chat session"""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.timestamp).all()

    return messages


@app.delete("/api/podcasts/{podcast_id}")
def delete_podcast(podcast_id: int, db: Session = Depends(get_db)):
    """Delete a podcast and its data"""
    podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")

    # Delete file
    if os.path.exists(podcast.file_path):
        os.remove(podcast.file_path)

    # Delete vector store
    vector_store.delete_podcast_collection(podcast_id)

    # Delete from database (cascade will handle related records)
    db.delete(podcast)
    db.commit()

    return {"message": "Podcast deleted successfully"}


@app.get("/")
async def root():
    """Serve the web interface"""
    return FileResponse("static/index.html")


# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
