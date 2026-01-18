
## Architectural & Design Decisions

This document captures the **key architectural decisions**, **trade-offs**, and **intentional constraints** behind the *Inhouse Document QA System*.
It exists to explain **why the system looks the way it does**, not just *what* it does.

---

## 1. Why Self-Hosted LLM Instead of Cloud APIs?

### Decision

Use a **self-hosted open-weight LLM** instead of OpenAI / Azure / Anthropic APIs.

### Rationale

* Enterprise data sensitivity and compliance
* Avoid data egress to third-party services
* Predictable cost model (no per-token billing)
* Full control over model behavior and upgrades

### Trade-offs

* Higher operational complexity
* Slower inference on CPU
* Responsibility for performance tuning

This project prioritizes **control and explainability over convenience**.

---

## 2. Why CPU-Only Execution?

### Decision

Run the LLM entirely on **CPU**, with no GPU dependency.

### Rationale

* Many enterprise laptops and servers lack GPUs
* GPU access is often restricted or shared
* CPU inference works everywhere
* Simplifies deployment and demo reproducibility

### Trade-offs

* High latency per request
* Low throughput
* Requires careful timeout management

CPU-only execution is **intentional**, not a limitation of skill.

---

## 3. Why GGUF + llama.cpp?

### Decision

Use **GGUF-formatted quantized models** served via **llama.cpp**.

### Rationale

* Optimized for CPU inference
* Smaller artifact sizes (4–5 GB)
* Reliable downloads via standard HTTPS
* No proprietary runtime dependencies
* Proven stability in enterprise environments

### Trade-offs

* Slower than GPU runtimes
* Fewer advanced serving features than vLLM/TGI

llama.cpp was chosen for **determinism and portability**, not raw performance.

---

## 4. Why Quantized Model (Q4_K_M)?

### Decision

Use a **quantized Mistral 7B Instruct model (Q4_K_M)**.

### Rationale

* Fits in typical 16 GB RAM machines
* Acceptable generation quality for document QA
* Faster inference than full-precision models
* Enables local development without specialized hardware

### Trade-offs

* Slight loss in generation quality
* Less suitable for creative tasks

For factual, document-grounded QA, this trade-off is acceptable.

---

## 5. Why Sentence-Transformer Embeddings Instead of LLM Embeddings?

### Decision

Use **Sentence Transformers (`all-MiniLM-L6-v2`)** for embeddings.

### Rationale

* CPU-efficient
* Fast embedding generation
* Well-tested for semantic search
* Decouples embedding pipeline from LLM runtime
* Avoids loading large LLMs just for embeddings

### Trade-offs

* Separate model lifecycle
* Requires embedding dimensional alignment

This separation improves **system modularity**.

---

## 6. Why FAISS for Vector Search?

### Decision

Use **FAISS (in-memory)** for vector similarity search.

### Rationale

* Lightweight and fast
* No external services required
* Suitable for small–medium document corpora
* Easy to reason about and debug

### Trade-offs

* No persistence across restarts (by design for now)
* Not horizontally scalable
* No built-in metadata filtering

FAISS was chosen to keep the system **simple and transparent**.

---

## 7. Why Manual Document Ingestion?

### Decision

Documents are **manually added** to a local `documents/` folder and ingested at startup.

### Rationale

* Simplifies the ingestion pipeline
* Avoids file upload edge cases
* Keeps focus on RAG correctness
* Suitable for demos and internal tools

### Trade-offs

* No dynamic ingestion
* Requires restart to pick up new documents

This decision was made to **reduce complexity without reducing learning value**.

---

## 8. Why Chunking Strategy (Overlapping Chunks)?

### Decision

Split documents into **overlapping text chunks**.

### Rationale

* Preserves semantic continuity across chunk boundaries
* Improves retrieval quality
* Reduces risk of partial context loss

### Trade-offs

* Increased number of stored vectors
* Slightly higher memory usage

Chunking parameters are tuned for **retrieval accuracy**, not minimal storage.

---

## 9. Why Explicit Hallucination Control?

### Decision

Force the model to answer **only from retrieved context**, otherwise say *“I don’t know.”*

### Rationale

* In-house document QA must not hallucinate
* Incorrect answers are worse than no answers
* Aligns with enterprise trust requirements

### Trade-offs

* More conservative responses
* Less “helpful” behavior for out-of-scope questions

This behavior is **intentional and desirable**.

---

## 10. Why No UI (Yet)?

### Decision

No Streamlit or web UI is included in the current version.

### Rationale

* Focus on backend correctness and architecture
* Avoid UI-driven complexity
* API-first design allows multiple frontends later

### Trade-offs

* Requires curl or Swagger for interaction

UI is intentionally deferred.

---

## 11. Why Metrics Are Not Implemented Yet?

### Decision

Metrics and observability are **planned but not implemented**.

### Rationale

* Core system correctness comes first
* Metrics without scale provide limited insight
* Avoid premature instrumentation

Planned metrics include:

* Retrieval latency
* LLM inference latency
* Token counts
* Memory usage

---

## 12. What Would Change in Production?

If this system were productionized:

* CPU → GPU inference
* FAISS → persistent vector database
* Manual ingestion → batch or API-driven ingestion
* Add authentication and access control
* Add observability and alerting
* Add caching and concurrency controls

The **core RAG architecture would remain unchanged**.

---

## Final Note

Every decision in this project was made to prioritize:

* **Explainability**
* **Determinism**
* **Enterprise realism**
* **Learning value**

This system is intentionally **simple, correct, and defensible**, rather than over-engineered.

---
