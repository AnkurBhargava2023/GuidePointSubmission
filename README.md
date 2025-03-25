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

---
# Project Structure

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


---

## Features

- **Multi-Field Indexing:** Documents are enriched with metadata (title and source) during loading and chunking.
- **Hybrid Search:** Combines semantic search (via embeddings) and lexical search (via BM25) for better query relevance.
- **FastAPI API:** An asynchronous API provides endpoints for querying the index with proper validation and error handling.
- **Latency Analysis:** Middleware and endpoint-level measurements capture API performance.
- **CI Pipeline:** Automated testing and release branch creation using GitHub Actions.
  
---

## Installation

Clone the repository:

git clone https://github.com/AnkurBhargava2023/GuidePointSubmission.git
cd your-repo

Install Dependencies:

pip install -r requirements.txt

Set up PDF files:

Place your PDF documents in a folder (Here it is kept at "/Users/ankurbhargava/Downloads/GuidePointFinalSubmission/Files" 


## Usage
Running the API

Start the API Server:

uvicorn api.main:app --reload

The API will be available at http://127.0.0.1:8000.

Test the API:

Navigate to http://127.0.0.1:8000/docs for interactive API documentation.

Use the /query endpoint to send POST requests with your search queries.

Example Query (Using Postman or curl)

curl -X POST "http://127.0.0.1:8000/query" \
 -H "Content-Type: application/json" \
 -d '{"query": "What is AI?", "search_type": "semantic"}'


## API Endpoints

GET /
Returns a welcome message.

POST /query
Accepts a JSON payload:

{
 	  "query": "Your search query",
      "search_type": "semantic" // or "lexical", "hybrid"
}

Returns a response containing:

A list of documents with title, source, and a snippet of content.

The latency (in seconds) for processing the query.


## CI/CD Pipeline

The CI/CD pipeline is set up using GitHub Actions. The workflow is defined in .github/workflows/ci-pipeline.yml and performs the following:

    On Push and PR to main:

        Checks out the repository.

        Sets up Python and installs dependencies.

        Runs a dummy test (tests/dummy_test.py).

    Release Branch Creation:

        After tests pass, a job creates (or updates) a release branch automatically.

Dummy Test Example (tests/dummy_test.py)

def test_dummy():
    assert 1 + 1 == 2

## Latency Analysis

Latency is measured in two ways:

Middleware Logging:

        Every incoming request is intercepted by a middleware that logs the total time taken (latency) for processing the request. This is logged to the console using the logging module.

Endpoint Measurement:

        The /query endpoint records the start time before processing and calculates the total processing time once the query is processed. This value is returned in the API response as latency.

#
