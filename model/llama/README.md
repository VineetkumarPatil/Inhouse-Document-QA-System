# Local LLM Runtime (llama.cpp)

This module contains the **local LLM inference runtime** powered by `llama.cpp`.

## Responsibilities

- Serve a quantized GGUF model via HTTP
- Perform CPU-only inference
- Provide health and readiness endpoints

## Model Characteristics

- Model: Mistral 7B Instruct
- Format: GGUF
- Quantization: Q4_K_M
- Execution: CPU-only

## Why This Exists Separately

- Decouples model serving from RAG logic
- Allows independent replacement (e.g. GPU runtimes)
- Keeps the backend API lightweight

## Notes

Model files are not committed to the repository.
They must be downloaded manually and mounted at runtime.
