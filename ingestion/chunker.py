from typing import List


class TextChunker:
    """
    Splits text into overlapping chunks.
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        words = text.split()
        chunks = []

        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            if chunk_text.strip():
                chunks.append(chunk_text)

            start += self.chunk_size - self.overlap

        return chunks
