# Semantic Catalogue System Architecture

## Overview
The Semantic Catalogue is a data discovery and explanation system that helps users find and understand relevant datasets through natural language queries. The system combines search, retrieval, and generative AI capabilities to provide contextual explanations of datasets.

## Key Components

### 1. Data Ingestion Pipeline
- **Data Sources**: ADR, UKDS, CDRC
- **ETL Process**:
  - Metadata extraction from APIs
  - Document processing (PDFs, text files)
  - Data cleaning and normalization
- **Storage**:
  - Parquet files for metadata
  - Raw documents in structured directories

### 2. Vector Search Infrastructure
- **Embedding Model**: OpenAI embeddings
- **Vector Store**: Pinecone hybrid search
- **Indexing**:
  - Chunking with TokenTextSplitter
  - BM25 sparse encoding
  - Vector embeddings for dense search

### 3. Core Processing Components
- **Search Graph**:
  - Query processing
  - Hybrid document retrieval
  - Relevance scoring and ranking
- **Generation Graph**:
  - Dataset explanation generation with inline citations
  - Hallucination detection
  - Content moderation
  - Iterative refinement

### 4. API Layer
- **FastAPI**:
  - REST endpoints for search/explain
  - CORS support
  - Thread-based session management
- **Endpoints**:
  - `/query` - Dataset search
  - `/explain` - Dataset explanation

### 5. AI/ML Components
- **LLM Integration**:
  - OpenAI GPT for generation
  - Structured output parsing
- **Chains**:
  - RAG (Retrieval Augmented Generation)
  - Citation generation
  - Hallucination checking
  - Content moderation
  - Explanation refinement (if hallucinated)

### 6. Orchestration & Scheduling
- **Dagster**:
  - Data pipeline orchestration
  - Asset management
  - Scheduled jobs for data updates
- **Jobs**:
  - ADR data sync
  - UKDS data sync
  - CDRC data sync
  - Vector index updates

### 7. Testing & Validation
- Unit tests for:
  - Search functionality
  - Generation chains
  - Hallucination detection
  - Content moderation
  - API endpoints
- Integration tests for:
  - Data pipelines
  - Vector search
  - End-to-end workflows

## Data Flow

1. User Query → API → Search Graph → Document Retrieval
2. Retrieved Documents → Generation Graph → Explanation Generation
3. Explanation → Moderation → Hallucination Check → Final Output

## Deployment Architecture

- **Containerized Services**:
  - FastAPI service (Containerfile.fastapi)
  - Dagster service (Containerfile.dagster)
- **Container Runtime Options**:
  - Docker (default)
  - Podman (alternative):
    - Use `podman-compose` instead of `docker-compose`
    - Set `DOCKER_HOST` environment variable if using rootless mode
    - Add `--security-opt label=disable` to container runs
    - Network configuration may require additional setup
- **Dependencies**:
  - Python 3.12
  - UV package manager
  - NLTK for text processing
- **Configuration**:
  - TOML-based config management
  - Environment variables for secrets

## Podman Considerations

When using Podman instead of Docker:

1. Installation:
   ```bash
   sudo apt-get install podman podman-docker podman-compose
   ```

2. Rootless Mode:
   - Configure subuids/subgids for your user
   - Set appropriate ulimits
   - May require additional network configuration

3. Compatibility:
   - Most Docker commands work with `podman` alias
   - Use `podman-compose` for compose files
   - Volume mounts may require different permissions

4. Networking:
   - Podman uses a different network stack
   - May need to configure firewall rules
   - Rootless containers use slirp4netns by default

## Key Technologies

- **Core Frameworks**:
  - LangChain/LangGraph
  - FastAPI
  - Dagster
- **AI/ML**:
  - OpenAI API
  - Pinecone
- **Data Processing**:
  - Polars
  - PDFMiner
- **Infrastructure**:
  - Docker
  - Pinecone Serverless
  - AWS (via Pinecone)

## Monitoring & Logging

- **Logging**:
  - Loguru for application logging
  - Rotating logs with retention
- **Monitoring**:
  - Dagster asset monitoring
  - API request tracking
  - Error logging
