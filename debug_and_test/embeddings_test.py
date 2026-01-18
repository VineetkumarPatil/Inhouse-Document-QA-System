from ingestion.embedder import TextEmbedder

embedder = TextEmbedder()

vec = embedder.embed("Hello world")
print("Vector length:", len(vec))
print("First 5 values:", vec[:5])
