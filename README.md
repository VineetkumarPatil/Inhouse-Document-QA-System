
# Inhouse Document QA System

**Self-Hosted LLM + Retrieval Augmented Generation (CPU, Docker, FastAPI)**

---

## 📌 Overview

This project implements a **fully self-hosted, in-house Document Question Answering (QA) system** designed under **enterprise constraints**:

* No external LLM APIs (OpenAI, Azure, etc.)
* CPU-only execution (no GPU dependency)
* Corporate-network compatibility
* Deterministic and explainable behavior
* Explicit control over hallucinations

The system combines:

* **Local LLM inference (llama.cpp)**
* **Document ingestion and chunking**
* **Vector embeddings and semantic retrieval**
* **Retrieval Augmented Generation (RAG)**
* **FastAPI inference gateway**

All components run **locally** and can be reasoned about independently.

---

## 🧩 Phases Completed

### ✅ Phase 1 — Self-Hosted LLM Serving

* llama.cpp HTTP server
* Quantized GGUF model (CPU-friendly)
* Dockerized deployment
* Health and readiness endpoints
* Works behind restricted corporate networks

---

### ✅ Phase 2 — FastAPI Inference Gateway *(core routing complete; metrics pending)*

* FastAPI backend
* `/query` endpoint
* Clean request/response schema
* Integration with local LLM
* Explicit timeout handling for CPU inference

> Metrics and tracing are intentionally deferred.

---

### ✅ Phase 3 — Embeddings Pipeline

* Sentence-Transformer embeddings (`all-MiniLM-L6-v2`)
* CPU-friendly execution
* Query and document embeddings
* Normalized vectors for cosine similarity

---

### ✅ Phase 4 — Vector Database & Semantic Retrieval

* FAISS in-memory vector store
* Cosine similarity search
* Top-K retrieval
* Score-based relevance interpretation

---

### ✅ Phase 5 — Retrieval Augmented Generation (RAG) Orchestration

* Manual document ingestion (TXT files)
* Overlapping chunking strategy
* Context construction
* Prompt grounding
* Hallucination prevention (“I don’t know” behavior)

This phase represents the **core system capability**.

---

## 🔜 Future Scope / Optional Phases

⬜ Phase 6 — Streamlit UI
⬜ Phase 7 — Observability, Optimization, and Scaling Notes


---

## 🧠 High-Level Architecture

## High-Level Architecture

![Document QA Architecture](documentation/architecture.png)

## Query Lifecycle and Component Responsibilities

### User Input

* **Input:** Natural language question
* **Guarantee:** UTF-8 text, non-empty

---

### API Layer — FastAPI (`/query`)

* **Responsibility:** Request validation and orchestration
* **Input:** User question
* **Output:** Structured QA response

---

### Embedding Layer

* **Responsibility:** Convert question text into a vector representation
* **Input:** Question string
* **Output:** Fixed-dimension embedding vector

---

### Retrieval Layer — FAISS

* **Responsibility:** Semantic similarity search
* **Input:** Query embedding
* **Output:** Top-K ranked document chunks

---

### Context Assembly

* **Responsibility:** Prepare retrieval output for prompting
* **Input:** Ranked document chunks
* **Output:** Ordered, bounded context window

---

### Prompt Construction

* **Responsibility:** Enforce grounding constraints
* **Input:** User question + context
* **Output:** Deterministic, source-bound prompt

---

### Inference Layer — Local LLM (`llama.cpp`)

* **Responsibility:** Generate answer using provided context only
* **Input:** Grounded prompt
* **Output:** Natural language answer

---

### Response

* **Guarantee:** Answer is derived solely from internal documents
* **Failure Mode:** Explicit *“not found in documents”* response

---

### System Invariant

All generated responses must be grounded exclusively in retrieved document context. No external knowledge is permitted.




---

## 🧠 Model & Runtime

### LLM

* **Model**: Mistral 7B Instruct
* **Format**: GGUF
* **Quantization**: Q4_K_M
* **Runtime**: llama.cpp (HTTP server)
* **Execution**: CPU-only

### Embeddings

* **Model**: `sentence-transformers/all-MiniLM-L6-v2`
* **Dimensions**: 384
* **Execution**: CPU-only

---

## 📁 Document Ingestion Model

For demo and clarity purposes, documents are **manually added**.

```
documents/
├── policies.txt
├── handbook.txt
└── internal_notes.txt
```

### Ingestion Flow

1. Load `.txt` files from `documents/`
2. Split into overlapping chunks
3. Generate embeddings per chunk
4. Store embeddings in FAISS index

Documents are ingested **once at application startup**.

---

## 🔍 What “Context” Means in Responses

In RAG responses, **context** refers to:

> The top-K document chunks retrieved via vector similarity search and provided to the LLM.

Example:

```dict
"context": [
  "Internal Notes RAG System Overview...",
  "Company Policies Data Privacy Policy..."
]
```

The LLM **only sees this context**, not the entire document corpus.

---

## 📊 What “Scores” Mean

Scores are **cosine similarity values** between:

* the question embedding
* each retrieved chunk embedding

Interpretation:

* `> 0.3` → strong semantic relevance
* `~ 0.0` → weak match
* `< 0.0` → unrelated

Scores influence **retrieval ranking**, not generation.

---

## 🚫 Hallucination Control

The system is explicitly designed to **avoid hallucinations**.

If the answer is **not present in retrieved documents**, the model responds:

> **“I don’t know.”**

This is enforced via:

* Prompt constraints
* Retrieval grounding
* No external knowledge access

---

## 🧰 Technology Stack

| Layer            | Technology              |
| ---------------- | ----------------------- |
| LLM Runtime      | llama.cpp               |
| Model Format     | GGUF (quantized)        |
| Backend API      | FastAPI                 |
| Embeddings       | Sentence Transformers   |
| Vector Search    | FAISS                   |
| Containerization | Docker                  |
| OS               | Windows + WSL2 (Ubuntu) |
| Hardware         | CPU-only                |

---

## ▶️ How to Run

### 1️⃣ Start LLM Server

```bash
docker run -p 8080:8080 \
  -v "/absolute/path/to/model/llama/models:/models" \
  mistral-llama
```

Verify:

```bash
curl http://localhost:8080/health
```

---

### 2️⃣ Start Backend API

From project root:

```bash
uvicorn backend.app.main:app --reload
```

Expected startup log:

```
[Startup] Ingested X document chunks
```

---

### 3️⃣ Query the System

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Retrieval Augmented Generation?"}'
```

---

## ⚙️ Performance Characteristics

* CPU inference latency: high (expected)
* Memory usage: ~7–9 GB RAM
* Throughput: suitable for demos and internal tools
* Behavior: deterministic and explainable

This system prioritizes **correctness and transparency over speed**.

---

## 📈 Why This Design

This project intentionally emphasizes:

* Explicit data flow
* Clear separation of concerns
* Enterprise realism
* Explainability over abstraction

Each component can later be replaced:

* CPU → GPU
* FAISS → managed vector database
* llama.cpp → vLLM / TGI
* Manual ingestion → automated pipelines

Without changing the RAG architecture.

---

## 🧠 Key Takeaway

This project demonstrates a **production-realistic, self-hosted RAG system** that:

* Works without cloud dependencies
* Respects enterprise constraints
* Prevents hallucinations
* Is fully explainable end-to-end

---
