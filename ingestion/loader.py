from pathlib import Path


class DocumentLoader:
    """
    Responsible for loading raw text content from text files.
    Only files with a `.txt` extension are supported.
    """

    def load(self, path: str) -> str:
        """
        Load and return the contents of a text file.

        Args:
            path (str): Path to the `.txt` file to be loaded.

        Returns:
            str: The raw text content of the file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file extension is not `.txt`.
        """
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if file_path.suffix.lower() != ".txt":
            raise ValueError("Only .txt files are supported")

        return file_path.read_text(encoding="utf-8", errors="ignore")
