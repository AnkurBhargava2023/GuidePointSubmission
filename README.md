# PDF Q&A System

This repository contains a solution for a PDF-based question answering system built using FastAPI and LangChain. The project is divided into two main parts:

- **Part 1:** Build an index by parsing, embedding, and indexing PDF documents. The index supports multi-field metadata (e.g., title and source) and hybrid search (combining semantic and lexical search).
- **Part 2:** Expose the index via an API with asynchronous processing, error handling, data validation, and performance measurement. Additionally, a CI pipeline is set up using GitHub Actions with a dummy test and an automated release branch.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [CI/CD Pipeline](#cicd-pipeline)
- [Latency Analysis](#latency-analysis)
- [License](#license)

---

## Project Overview

This project is a robust PDF Q&A system that:
- **Parses PDF files** using PyPDFLoader and extracts metadata (title and source).
- **Chunks documents** into manageable pieces while preserving metadata.
- **Embeds text** using pre-trained models (BGE or Universal Sentence Encoder) via LangChain.
- **Indexes document chunks** in a Chroma vector database.
- **Performs hybrid search** by combining semantic (vector) and lexical (BM25) retrieval techniques.
- **Exposes an API** via FastAPI with asynchronous handling, data validation, error handling, and latency logging.
- **Includes a CI/CD pipeline** on GitHub Actions with a dummy test and automated release branch creation.

---

## Features

- **Multi-Field Indexing:** Documents are enriched with metadata (title and source) during loading and chunking.
- **Hybrid Search:** Combines semantic search (via embeddings) and lexical search (via BM25) for better query relevance.
- **FastAPI API:** An asynchronous API provides endpoints for querying the index with proper validation and error handling.
- **Latency Analysis:** Middleware and endpoint-level measurements capture API performance.
- **CI Pipeline:** Automated testing and release branch creation using GitHub Actions.
  
---

## Project Structure

```plaintext
project_root/
├── api/
│   ├── __init__.py             # (Can be empty or expose API-level objects)
│   └── main.py                 # FastAPI application with endpoints and latency logging
├── app/
│   ├── __init__.py             # Exports key modules (PDFLoader, chunk_documents, etc.)
│   ├── pdf_loader.py           # Loads PDFs using PyPDFLoader, attaches metadata (title, source)
│   ├── chunking.py             # Splits Document objects into chunks, preserving metadata
│   ├── embeddings.py           # Loads embedding models (USE/BGE) via LangChain
│   ├── indexer.py              # Indexes chunked documents into Chroma vector store
│   └── search.py               # Contains the Retriever class for semantic, lexical, and hybrid search
├── config.py                   # Global configuration (persist directory, weights, chunking parameters, etc.)
├── .github/
│   └── workflows/
│       └── ci-pipeline.yml     # GitHub Actions workflow for CI/CD pipeline
├── tests/
│   └── dummy_test.py           # A dummy test for CI pipeline
├── requirements.txt            # List of project dependencies
└── README.md                   # Project documentation (this file)

