from openai import OpenAI
from typing import List, Dict
import os
from dotenv import load_dotenv
from vector_store import VectorStore

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatbotService:
    def __init__(self):
        self.vector_store = VectorStore()

    def generate_response(
        self,
        podcast_id: int,
        user_query: str,
        chat_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate a chatbot response based on the podcast transcription

        Args:
            podcast_id: ID of the podcast
            user_query: User's question
            chat_history: Previous chat messages

        Returns:
            Generated response
        """
        # Search for relevant context from transcription
        relevant_chunks = self.vector_store.search(podcast_id, user_query, n_results=5)

        if not relevant_chunks:
            return "I don't have enough information from this podcast to answer your question."

        # Build context from relevant chunks
        context = "\n\n".join([chunk['text'] for chunk in relevant_chunks])

        # Build messages for the chat
        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful AI assistant that answers questions about podcast content.
You have access to the following transcription excerpts from the podcast:

{context}

Answer the user's questions based on this content. If the answer is not in the provided excerpts,
say so. Be conversational and helpful. Cite specific parts of the transcription when relevant."""
            }
        ]

        # Add chat history
        if chat_history:
            messages.extend(chat_history[-6:])  # Include last 6 messages for context

        # Add current user query
        messages.append({"role": "user", "content": user_query})

        # Generate response
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def summarize_transcription(self, transcription_text: str) -> str:
        """
        Generate a summary of the podcast transcription

        Args:
            transcription_text: Full transcription text

        Returns:
            Summary text
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that summarizes podcast transcriptions."
                    },
                    {
                        "role": "user",
                        "content": f"Please provide a concise summary of this podcast transcription:\n\n{transcription_text[:4000]}"
                    }
                ],
                temperature=0.5,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"
