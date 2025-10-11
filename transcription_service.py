import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def transcribe_audio(audio_file_path: str) -> dict:
    """
    Transcribe audio file using OpenAI Whisper API

    Args:
        audio_file_path: Path to the audio file

    Returns:
        dict with 'text' and 'duration' keys
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )

        return {
            "text": transcript.text,
            "duration": int(transcript.duration) if hasattr(transcript, 'duration') else None
        }
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Split text into overlapping chunks for better semantic search

    Args:
        text: The full transcription text
        chunk_size: Size of each chunk in characters
        overlap: Overlap between chunks in characters

    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks
