import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()


class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def create_collection_for_podcast(self, podcast_id: int, transcription_text: str):
        """
        Create a vector store collection for a podcast transcription

        Args:
            podcast_id: ID of the podcast
            transcription_text: Full transcription text
        """
        collection_name = f"podcast_{podcast_id}"

        # Delete collection if it exists
        try:
            self.client.delete_collection(name=collection_name)
        except:
            pass

        # Create new collection
        collection = self.client.create_collection(name=collection_name)

        # Split text into chunks
        chunks = self.text_splitter.split_text(transcription_text)

        # Generate embeddings and add to collection
        for i, chunk in enumerate(chunks):
            embedding = self.embeddings.embed_query(chunk)
            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                ids=[f"chunk_{i}"]
            )

        return len(chunks)

    def search(self, podcast_id: int, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search for relevant chunks in the podcast transcription

        Args:
            podcast_id: ID of the podcast
            query: Search query
            n_results: Number of results to return

        Returns:
            List of relevant text chunks with metadata
        """
        collection_name = f"podcast_{podcast_id}"

        try:
            collection = self.client.get_collection(name=collection_name)
        except:
            return []

        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)

        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'text': doc,
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })

        return formatted_results

    def delete_podcast_collection(self, podcast_id: int):
        """Delete the vector store collection for a podcast"""
        collection_name = f"podcast_{podcast_id}"
        try:
            self.client.delete_collection(name=collection_name)
        except:
            pass
