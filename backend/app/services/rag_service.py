from typing import Any, Dict, List

import httpx

from ingestion.embedder import TextEmbedder
from ingestion.vector_store import VectorStore


class RAGService:
    """
    Retrieval-Augmented Generation (RAG) service.

    This service embeds user queries, retrieves relevant context from
    a vector store, constructs a prompt, and queries a local LLM
    endpoint to generate an answer grounded in retrieved context.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        llm_url: str = "http://localhost:8080/completion",
    ):
        """
        Initialize the RAG service.

        Args:
            vector_store (VectorStore): The vector store used for similarity search.
            llm_url (str): URL of the local LLM completion endpoint.
        """
        self.vector_store = vector_store
        self.embedder = TextEmbedder()
        self.llm_url = llm_url

    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Answer a question using retrieval-augmented generation.

        The method embeds the question, retrieves the most relevant
        document chunks, builds a constrained prompt, sends it to
        a local LLM server, and returns the generated answer along
        with supporting context and similarity scores.

        Args:
            question (str): The user question to be answered.
            top_k (int): Number of top relevant context chunks to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing the original question,
            generated answer, retrieved context chunks, and similarity scores.

        Raises:
            RuntimeError: If the LLM request times out or fails.
        """
        # 1️. Embed the question
        query_embedding = self.embedder.embed(question)

        # 2️. Retrieve top-k chunks
        results = self.vector_store.search(query_embedding, top_k=top_k)

        if not results:
            return {
                "question": question,
                "answer": "I don't know.",
                "context": [],
                "scores": [],
            }

        contexts: List[str] = [text for text, _ in results]
        scores: List[float] = [score for _, score in results]

        # 3️. Build prompt (keeping it SHORT)
        context_block = "\n\n".join(contexts)

        prompt = f"""
You are a helpful assistant.
Answer the question ONLY using the context below.
If the answer is not in the context, say "I don't know".

Context:
{context_block}

Question:
{question}

Answer:
""".strip()

        # 4. Call local llama.cpp server (CPU-safe)
        payload = {
            "prompt": prompt,
            "n_predict": 80,  # small output
            "temperature": 0.2,
            "top_p": 0.9,
            "stop": ["</s>"],
        }

        try:
            response = httpx.post(
                self.llm_url,
                json=payload,
                timeout=httpx.Timeout(180.0),  # long timeout
            )
            response.raise_for_status()
        except httpx.TimeoutException:
            raise RuntimeError("LLM request timed out (CPU inference is slow)")
        except httpx.HTTPError as e:
            raise RuntimeError(f"LLM request failed: {str(e)}")

        data = response.json()

        answer = data.get("content", "").strip()
        if not answer:
            answer = "I don't know."

        return {
            "question": question,
            "answer": answer,
            "context": contexts,
            "scores": scores,
        }
