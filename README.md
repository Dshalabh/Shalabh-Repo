# 🎙️ Shalabh's Podcast Chat

### AI-Powered Podcast Transcription & Chat Application

A web application that allows you to upload podcasts, automatically transcribe them, and chat with an AI about the content using semantic search.

**Created by:** Shalabh Dongaonkar
**Built with:** Claude Code by Anthropic

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

- 🎙️ **Podcast Upload**: Upload audio files in multiple formats (MP3, WAV, M4A, etc.)
- 📝 **Automatic Transcription**: Uses OpenAI Whisper API to transcribe audio
- 🔍 **Semantic Search**: Vector embeddings for intelligent content retrieval
- 💬 **Interactive Chat**: Ask questions about podcast content with context-aware responses
- 💾 **Database Storage**: SQLite database for managing podcasts and chat history
- 🎨 **Modern UI**: Clean, responsive web interface
- 📦 **Large File Support**: Automatically handles files > 25MB by splitting into chunks
- 🌐 **Custom Domain**: Use friendly URLs like `podcastbot.local` instead of `localhost`

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Navigate to the project directory**:
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
     ```env
     OPENAI_API_KEY=sk-your-key-here
     DATABASE_URL=sqlite:///./podcast_chatbot.db
     UPLOAD_DIR=./uploads
     ```

5. **Run the application**:
   ```bash
   python PODCASTBOT.py
   ```

6. **Access the app**:
   - Open your browser: `http://localhost:8000`
   - Or use custom domain: `http://podcastbot.local:8000` (see below)

## 🌐 Custom Domain Setup (Optional)

Instead of using `http://localhost:8000`, you can use a friendly URL like `http://podcastbot.local:8000`!

### Quick Setup (Automatic)

Run the setup script as Administrator:
```bash
setup_domain.bat
```

Choose option 1 for `podcastbot.local` and you're done!

### Manual Setup

1. **Open Notepad as Administrator**
2. **Open file**: `C:\Windows\System32\drivers\etc\hosts`
3. **Add this line**:
   ```
   127.0.0.1    podcastbot.local
   ```
4. **Save and run**: `ipconfig /flushdns`
5. **Access**: `http://podcastbot.local:8000`

📖 **Full guide**: See [CUSTOM_DOMAIN_SETUP.md](CUSTOM_DOMAIN_SETUP.md) for detailed instructions

## 📖 Usage

### 1. Upload a Podcast

- Enter a title
- Select an audio file (any size - large files automatically handled!)
- Click "Upload Podcast"
- Wait for transcription to complete (status will update automatically)

### 2. Chat with the Podcast

- Click on a completed podcast
- Ask questions about the content
- The AI will provide context-aware answers based on the transcription

### Example Questions

- "What are the main topics discussed in this podcast?"
- "Can you summarize the key points?"
- "What did they say about [specific topic]?"
- "Who are the speakers and what are their perspectives?"

## 🏗️ Architecture

### Backend Components

1. **Database Layer** ([database.py](database.py))
   - SQLAlchemy models for Podcasts, Transcriptions, ChatSessions, and ChatMessages
   - SQLite database with proper relationships

2. **Transcription Service** ([transcription_service.py](transcription_service.py))
   - OpenAI Whisper API integration
   - Automatic audio file splitting for large files (> 25MB)
   - Audio file processing with pydub

3. **Vector Store** ([vector_store.py](vector_store.py))
   - ChromaDB for vector embeddings
   - OpenAI embeddings for semantic search
   - Text chunking for better retrieval

4. **Chatbot Service** ([chatbot_service.py](chatbot_service.py))
   - GPT-4 integration for conversational responses
   - Context-aware responses using retrieved chunks
   - Chat history management

5. **API Layer** ([PODCASTBOT.py](PODCASTBOT.py)) ⭐
   - FastAPI REST endpoints
   - Background task processing
   - File upload handling

### Frontend

- Modern, responsive single-page application ([static/index.html](static/index.html))
- Real-time status updates
- Conversational chat interface

## 🔌 API Endpoints

### Podcasts

- `POST /api/podcasts/upload` - Upload a new podcast
- `GET /api/podcasts` - List all podcasts
- `GET /api/podcasts/{podcast_id}` - Get podcast details
- `GET /api/podcasts/{podcast_id}/transcription` - Get transcription
- `DELETE /api/podcasts/{podcast_id}` - Delete podcast

### Chat

- `POST /api/podcasts/{podcast_id}/chat` - Send a chat message
- `GET /api/sessions/{session_id}/messages` - Get chat history

### Documentation

- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)
- `GET /api/health` - Health check endpoint

## 📊 Database Schema

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

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.9+
- **Database**: SQLAlchemy, SQLite
- **AI/ML**: OpenAI (Whisper, GPT-4, Embeddings)
- **Vector Store**: ChromaDB
- **Audio Processing**: pydub
- **Frontend**: HTML, CSS, JavaScript (Vanilla)

## 💡 How It Works

1. **Upload**: User uploads a podcast audio file
2. **Transcription**: Background task transcribes audio using Whisper API
   - Files > 25MB are automatically split into chunks
   - Each chunk is transcribed separately
   - Transcripts are combined seamlessly
3. **Vectorization**: Transcription is split into chunks and embedded
4. **Chat**: User asks questions
5. **Retrieval**: Semantic search finds relevant chunks
6. **Response**: GPT-4 generates context-aware answer

## 💰 Cost Considerations

This application uses OpenAI APIs which incur costs:

- **Whisper API**: ~$0.006 per minute of audio
- **GPT-4**: Variable based on tokens used
- **Embeddings**: ~$0.0001 per 1K tokens

**Example:** A 1-hour podcast costs approximately:
- Transcription: $0.36
- Initial embeddings: ~$0.02
- Chat messages: $0.01-0.10 per conversation
- **Total: ~$0.40-0.60**

## ⚙️ Configuration

Environment variables in `.env`:

```env
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (defaults provided)
DATABASE_URL=sqlite:///./podcast_chatbot.db
UPLOAD_DIR=./uploads
```

## 🐛 Troubleshooting

### Transcription Fails

- ✅ Check OpenAI API key is valid
- ✅ Ensure audio file format is supported
- ✅ Large files (> 25MB) are now automatically handled!

### Chat Not Working

- ✅ Verify transcription status is "completed"
- ✅ Check OpenAI API key has GPT-4 access
- ✅ Ensure vector store is initialized

### Database Errors

- ✅ Delete `podcast_chatbot.db` and restart to reset database
- ✅ Check file permissions in the project directory

### Custom Domain Not Working

- ✅ Run `ipconfig /flushdns`
- ✅ Clear browser cache
- ✅ Verify hosts file entry
- ✅ See [CUSTOM_DOMAIN_SETUP.md](CUSTOM_DOMAIN_SETUP.md)

### Upload Issues

- ✅ See [FIX_UPLOAD_ISSUES.md](FIX_UPLOAD_ISSUES.md) for detailed troubleshooting

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup guide (5 minutes)
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete architecture overview
- **[CUSTOM_DOMAIN_SETUP.md](CUSTOM_DOMAIN_SETUP.md)** - Custom URL configuration
- **[FIX_UPLOAD_ISSUES.md](FIX_UPLOAD_ISSUES.md)** - Upload troubleshooting guide
- **[CUSTOM_URL_QUICKSTART.txt](CUSTOM_URL_QUICKSTART.txt)** - Quick reference card

## 🎯 Limitations

- No user authentication (single-user application)
- No multi-user support
- Single-threaded background tasks
- No streaming responses
- Local storage only

## 🚀 Future Enhancements

- [ ] User authentication
- [ ] Multi-user support
- [ ] YouTube URL support
- [ ] RSS feed integration
- [ ] Speaker diarization
- [ ] Timestamp linking
- [ ] Transcription export (TXT, SRT, VTT)
- [ ] Multi-language support
- [ ] Streaming responses
- [ ] Cloud storage integration
- [ ] Docker containerization

## 📁 Project Structure

```
podcast_chatbot/
├── PODCASTBOT.py              ⭐ Main application file
├── database.py                Database models
├── transcription_service.py   Whisper integration + large file handling
├── vector_store.py            Vector embeddings
├── chatbot_service.py         GPT-4 chat logic
├── requirements.txt           Dependencies
├── .env.example              Environment template
├── static/
│   └── index.html            Web interface
├── uploads/                  Audio files
├── podcast_chatbot.db        SQLite database
└── docs/
    ├── README.md             This file
    ├── QUICKSTART.md         Quick setup
    ├── PROJECT_SUMMARY.md    Architecture
    ├── CUSTOM_DOMAIN_SETUP.md Custom URLs
    └── FIX_UPLOAD_ISSUES.md  Upload troubleshooting
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use and modify as needed.

## 🙏 Credits

- **Created by**: Shalabh Dongaonkar
- **Built with**: [Claude Code](https://claude.com/claude-code) by Anthropic
- **AI Services**: OpenAI (Whisper, GPT-4, Embeddings)
- **Vector Database**: ChromaDB
- **Text Processing**: LangChain
- **Audio Processing**: pydub

## 📞 Support

For issues or questions:
1. Check the documentation files
2. Review console output for error messages
3. Verify OpenAI API key and status
4. See troubleshooting guides

---

**Version:** 1.0.0
**Status:** Production Ready ✅
**Author:** Shalabh Dongaonkar

Enjoy your podcast chatbot! 🎙️✨

