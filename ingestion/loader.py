from pathlib import Path


class DocumentLoader:
    """
    Loads raw text from TXT files only.
    """

    def load(self, path: str) -> str:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if file_path.suffix.lower() != ".txt":
            raise ValueError("Only .txt files are supported")

        return file_path.read_text(encoding="utf-8", errors="ignore")
