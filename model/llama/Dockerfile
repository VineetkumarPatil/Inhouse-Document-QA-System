FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    curl \
    libcurl4-openssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/ggml-org/llama.cpp.git

WORKDIR /app/llama.cpp

RUN cmake -B build \
    && cmake --build build -j$(nproc)

RUN mkdir -p /models

EXPOSE 8080

CMD ["./build/bin/llama-server", "-m", "/models/model.gguf", "--host", "0.0.0.0", "--port", "8080"]
# CMD ["./build/bin/llama-server", "-m", "/models/model.gguf", "--host", "0.0.0.0", "--port", "8080", "--embeddings", "--threads", "6", "--batch-size", "256"]

