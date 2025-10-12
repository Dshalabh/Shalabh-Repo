# Podcast Chatbot - NotebookLM Style

A web application that allows you to upload podcasts, automatically transcribe them, and chat with an AI about the content using semantic search.

## Features

- 🎙️ **Podcast Upload**: Upload audio files in multiple formats (MP3, WAV, M4A, etc.)
- 📝 **Automatic Transcription**: Uses OpenAI Whisper API to transcribe audio
- 🔍 **Semantic Search**: Vector embeddings for intelligent content retrieval
- 💬 **Interactive Chat**: Ask questions about podcast content with context-aware responses
- 💾 **Database Storage**: SQLite database for managing podcasts and chat history
- 🎨 **Modern UI**: Clean, responsive web interface

## Architecture

### Backend Components

1. **Database Layer** (`database.py`)
   - SQLAlchemy models for Podcasts, Transcriptions, ChatSessions, and ChatMessages
   - SQLite database with proper relationships

2. **Transcription Service** (`transcription_service.py`)
   - OpenAI Whisper API integration
   - Audio file processing

3. **Vector Store** (`vector_store.py`)
   - ChromaDB for vector embeddings
   - OpenAI embeddings for semantic search
   - Text chunking for better retrieval

4. **Chatbot Service** (`chatbot_service.py`)
   - GPT-4 integration for conversational responses
   - Context-aware responses using retrieved chunks
   - Chat history management

5. **API Layer** (`main.py`)
   - FastAPI REST endpoints
   - Background task processing
   - File upload handling

### Frontend

- Modern, responsive single-page application
- Real-time status updates
- Conversational chat interface

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd C:\Users\ShalabDo\podcast_chatbot
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-key-here
     DATABASE_URL=sqlite:///./podcast_chatbot.db
     UPLOAD_DIR=./uploads
     ```

## Usage

1. **Start the server**:
   ```bash
   python main.py
   ```

   Or with uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open your browser**: **Access:**
- Web UI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

3. **Upload a podcast**:
   - Enter a title
   - Select an audio file
   - Click "Upload Podcast"
   - Wait for transcription to complete (status will update automatically)

4. **Chat with the podcast**:
   - Click on a completed podcast
   - Ask questions about the content
   - The AI will provide context-aware answers based on the transcription

## API Endpoints

### Podcasts

- `POST /api/podcasts/upload` - Upload a new podcast
- `GET /api/podcasts` - List all podcasts
- `GET /api/podcasts/{podcast_id}` - Get podcast details
- `GET /api/podcasts/{podcast_id}/transcription` - Get transcription
- `DELETE /api/podcasts/{podcast_id}` - Delete podcast

### Chat

- `POST /api/podcasts/{podcast_id}/chat` - Send a chat message
- `GET /api/sessions/{session_id}/messages` - Get chat history

## Database Schema

```
Podcast
├── id
├── title
├── filename
├── file_path
├── upload_date
└── transcription_status

Transcription
├── id
├── podcast_id (FK)
├── full_text
├── created_at
└── duration

ChatSession
├── id
├── podcast_id (FK)
└── created_at

ChatMessage
├── id
├── session_id (FK)
├── role (user/assistant)
├── content
└── timestamp
```

## Technology Stack

- **Backend**: FastAPI, Python 3.9+
- **Database**: SQLAlchemy, SQLite
- **AI/ML**: OpenAI (Whisper, GPT-4, Embeddings)
- **Vector Store**: ChromaDB
- **Frontend**: HTML, CSS, JavaScript (Vanilla)

## How It Works

1. **Upload**: User uploads a podcast audio file
2. **Transcription**: Background task transcribes audio using Whisper API
3. **Vectorization**: Transcription is split into chunks and embedded
4. **Chat**: User asks questions
5. **Retrieval**: Semantic search finds relevant chunks
6. **Response**: GPT-4 generates context-aware answer

## Limitations

- Requires OpenAI API key (costs apply)
- Audio file size limits depend on OpenAI Whisper API (25MB max)
- Processing time depends on audio length

## Future Enhancements

- Support for multiple audio sources (YouTube, RSS feeds)
- Speaker diarization
- Timestamp linking
- Export transcriptions
- Multi-language support
- User authentication

## Troubleshooting

**Transcription fails**:
- Check OpenAI API key is valid
- Ensure audio file format is supported
- Check file size is under 25MB

**Chat not working**:
- Verify transcription status is "completed"
- Check OpenAI API key has GPT-4 access
- Ensure vector store is initialized

**Database errors**:
- Delete `podcast_chatbot.db` and restart to reset database
- Check file permissions in the project directory

## License

MIT License - feel free to use and modify as needed.

