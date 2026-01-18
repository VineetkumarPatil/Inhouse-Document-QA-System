import httpx
from typing import List, Dict, Any

from ingestion.embedder import TextEmbedder
from ingestion.vector_store import VectorStore


class RAGService:
    """
    Retrieval Augmented Generation service.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        llm_url: str = "http://localhost:8080/completion",
    ):
        self.vector_store = vector_store
        self.embedder = TextEmbedder()
        self.llm_url = llm_url

    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        # 1️⃣ Embed the question
        query_embedding = self.embedder.embed(question)

        # 2️⃣ Retrieve top-k chunks
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

        # 3️⃣ Build prompt (keep it SMALL)
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

        # 4️⃣ Call local llama.cpp server (CPU-safe)
        payload = {
            "prompt": prompt,
            "n_predict": 80,          # 🔴 IMPORTANT: small output
            "temperature": 0.2,
            "top_p": 0.9,
            "stop": ["</s>"],
        }

        try:
            response = httpx.post(
                self.llm_url,
                json=payload,
                timeout=httpx.Timeout(180.0),  # 🔴 IMPORTANT: long timeout
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
