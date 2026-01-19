from typing import List


class TextChunker:
    """
    Utility class for splitting text into overlapping word-based chunks.
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        """
        Initialize the TextChunker.

        Args:
            chunk_size (int): The maximum number of words per chunk.
            overlap (int): The number of overlapping words between consecutive chunks.

        Raises:
            ValueError: If overlap is greater than or equal to chunk_size.
        """
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        """
        Split the input text into overlapping chunks of words.

        Args:
            text (str): The input text to be split into chunks.

        Returns:
            List[str]: A list of text chunks, each containing up to chunk_size words,
            with overlap words shared between consecutive chunks.
        """
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
