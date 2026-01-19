# Document Corpus

This directory contains the **source documents** used for question answering.

## Supported Format

- Plain text (`.txt`) files only

## Usage

- Documents are loaded at application startup
- Changes require a restart to take effect
- Each file is treated as an independent source

## Design Rationale

Manual document management avoids ingestion complexity
and keeps focus on retrieval and generation correctness.

This approach is suitable for demos and internal tools.
