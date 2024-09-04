# Semantic Catalogue

![GitHub release (latest by date)](https://img.shields.io/github/v/release/cjber/semantic-catalogue)
![GitHub last commit](https://img.shields.io/github/last-commit/cjber/semantic-catalogue)
![GitHub issues](https://img.shields.io/github/issues/cjber/semantic-catalogue)
![GitHub pull requests](https://img.shields.io/github/issues-pr/cjber/semantic-catalogue)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Docker](https://img.shields.io/badge/docker-available-blue)
![Dagster](https://img.shields.io/badge/dagster-1.7.8-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.112.0-blue)

## Overview

The Semantic Search Catalogue is a cutting-edge project designed to enhance the search capabilities of data catalogues for research purposes. By moving beyond traditional keyword-based searches, it provides users with more accurate and relevant results through semantic understanding.

## Features

- **Semantic Search:** Utilizes OpenAI embeddings stored on Pinecone, enabling semantic querying using cosine similarity for enhanced search accuracy.
- **Retrieval Augmented Generation:** Leverages GPT 3.5 turbo to generate responses that explain the relevance of retrieved datasets, offering deeper insights.
- **Automated Data Management:** Uses Dagster to automate the creation and management of the Pinecone vector database.
- **Multi-source Integration:** Aggregates data from multiple sources including ADR, CDRC, and UKDS.
- **Moderation and Hallucination Detection:** Ensures the generated content is appropriate and grounded in facts.

## System Architecture

The Semantic Catalogue employs a standard Retrieval Augmented Generation (RAG) architecture:

![System Architecture](./reports/figs/system.png)

Dagster is utilized to automate the creation of the Pinecone vector database, ensuring efficient data management:

![Global Asset Lineage](./reports/figs/Global_Asset_Lineage.svg)

## Project Structure

The project is organized into several key components:

- **Backend (FastAPI):** Handles API requests and integrates with the data processing pipeline.
- **Frontend (React):** Provides a user-friendly interface for interacting with the semantic search capabilities.
- **Data Processing (Dagster):** Manages data ingestion, processing, and storage using a robust pipeline.
- **Vector Database (Pinecone):** Stores embeddings for efficient semantic search.
- **Machine Learning Models (OpenAI):** Powers the semantic understanding and generation capabilities.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Docker or Podman
- Git

### Build Python Environment

To contribute, please follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cjber/semantic-catalogue.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd semantic-catalogue
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.lock
   ```

4. **Configure the system:**

   Edit the `config/config.toml` file to customize model settings.

## Running the Project

The project is fully containerized using `podman`/`docker` `compose`. To run the full system, execute:

```bash
podman compose up -d
```

### Accessing the Semantic Catalogue Search

Once up and running, access the semantic catalogue search at `http://localhost:8001`.

### Running the Dagster Pipeline

The Dagster UI is available at `http://localhost:3000`. Adjust the Auto Materialize and Sensor settings to start the automation.

> **WARNING:** This project is not intended for public use and requires access to a private database.

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Documentation

Further information regarding the methods used can be found in [DOCS.md](./reports/DOCS.md).

## Contact

For any inquiries, please contact the project maintainers at [contact@example.com](mailto:contact@example.com).

## Acknowledgements

- **OpenAI:** For providing the powerful language models.
- **Pinecone:** For the vector database services.
- **Dagster:** For the data orchestration framework.
- **FastAPI:** For the web framework.
- **LangChain:** For the seamless integration of language models.
- **Polars:** For efficient data manipulation.
- **React:** For building the frontend interface.
- **Material-UI:** For the UI components.
- **Docker:** For containerization.
- **PostgreSQL:** For the database management.
- **Tenacity:** For retrying operations.
- **TQDM:** For progress bars.
- **Requests:** For making HTTP requests.
- **Dateparser:** For parsing dates.
- **PDFMiner:** For extracting text from PDFs.
- **Pydantic:** For data validation.
- **Sickle:** For harvesting metadata.
