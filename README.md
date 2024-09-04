<div align="center">

![](./reports/figs/svg/logo-no-background.svg)

![GitHub last commit](https://img.shields.io/github/last-commit/cjber/semantic-catalogue?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/cjber/semantic-catalogue?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/cjber/semantic-catalogue?style=for-the-badge)

![Python Version](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Dagster](https://img.shields.io/badge/Dagster-654FF0?style=for-the-badge&logo=Dagster&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)


---
**The _Semantic Catalogue_ is a project designed to enhance the search capabilities of data catalogues for research purposes. By moving beyond traditional keyword-based searches, it provides users with more accurate and relevant results through semantic understanding.**

---


</div>


## Features

- **Semantic Search:** OpenAI embeddings stored on Pinecone enable semantic querying using cosine similarity for enhanced search discoverability.
- **Retrieval Augmented Generation:** GPT 4o-turbo generates responses that explain the relevance of retrieved datasets, enabling transparency and insights.
- **Moderation and Hallucination Detection:** Ensures the generated content is appropriate and grounded in facts.
- **Automated Data Management:** Dagster automates the creation and continuous management of the Pinecone vector database.

## System Architecture

The Semantic Catalogue employs a standard Retrieval Augmented Generation (RAG) architecture, which combines the strengths of retrieval-based and generation-based models. This architecture first retrieves relevant dataset descriptions based on a users query, then uses them to generate more accurate and contextually relevant responses to explain their relevance.

![System Architecture](./reports/figs/system.png)

Dagster is used to automate the creation and continuous management of the Pinecone vector database, ensuring efficient data management and seamless updates. This automation includes tasks such as data ingestion, transformation, and indexing, which are crucial for maintaining the accuracy and relevance of the semantic search capabilities:

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

### Contribution Setup

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

> [!WARNING]
> This project is not intended for public use and requires access to a private database.

The project is fully containerised using `podman`/`docker` `compose`. To run the full system, execute:

```bash
podman compose up -d
```

### Accessing the Frontend

Once up and running, access the semantic catalogue search at `http://localhost:8001`.

### Running the Dagster Pipeline

The Dagster UI is available at `http://localhost:3000`. Adjust the Auto Materialize and Sensor settings to start the automation.

