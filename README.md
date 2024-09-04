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

[Methodology](./reports/DOCS.md) · [View Demo](https://apps.cdrc.ac.uk/semantic-catalogue) · [Getting Started](https://github.com/cjber/semantic-catalogue?tab=readme-ov-file#getting-started)
</div>


## Overview

The Semantic Catalogue is an advanced system designed to enhance the search capabilities of data catalogues by leveraging semantic understanding. Unlike traditional keyword-based searches, this system uses semantic embeddings to provide users with more accurate and contextually relevant results. The project integrates several cutting-edge technologies, including OpenAI's language models, Pinecone's vector database, and Dagster's data orchestration capabilities, to deliver a comprehensive solution for semantic search and data management.

## Features

- **Semantic Search:** Utilizes OpenAI embeddings stored in Pinecone to perform semantic queries, enhancing search discoverability through cosine similarity.
- **Retrieval Augmented Generation (RAG):** Employs GPT 4o-turbo to generate responses that explain the relevance of retrieved datasets, providing transparency and insights.
- **Moderation and Hallucination Detection:** Ensures generated content is appropriate and factually grounded, using moderation and hallucination detection mechanisms.
- **Automated Data Management:** Leverages Dagster to automate the creation and continuous management of the Pinecone vector database, ensuring efficient data handling and updates.

## System Architecture

The Semantic Catalogue employs a Retrieval Augmented Generation (RAG) architecture, which combines retrieval-based and generation-based models. This involves two main steps:

1. **Retrieval:** Relevant datasets are retrieved based on a user's query using semantic embeddings.
2. **Generation:** The retrieved dataset descriptions are used to generate contextually relevant responses that explain their relevance to the query.

![System Architecture](./reports/figs/system.png)
*System Architecture*

- **Backend (FastAPI):** Handles API requests and integrates with the data processing pipeline. It serves as the core interface for interacting with the semantic search system.
- **Frontend (React):** Provides a user-friendly interface for users to interact with the semantic search capabilities. It allows users to input queries and view results in an intuitive manner.
- **Data Processing (Dagster):** Manages the entire data lifecycle, from ingestion to processing and storage. Dagster's robust pipeline ensures data is handled efficiently and accurately.
- **Vector Database (Pinecone):** Stores semantic embeddings for efficient search operations. Pinecone's vector database is optimized for handling high-dimensional data, making it ideal for semantic search tasks.
- **Machine Learning Models (OpenAI):** Powers the semantic understanding and generation capabilities. OpenAI's models are used to interpret queries and generate relevant responses based on retrieved data.

### Data Management with Dagster

Dagster automates the data management processes, including data ingestion, transformation, and indexing. This ensures the Pinecone vector database is continuously updated and maintained, which is crucial for the accuracy and relevance of the semantic search capabilities.

![Global Asset Lineage](./reports/figs/Global_Asset_Lineage.svg)
*Global Asset Lineage*


## Detailed Functionality

### Semantic Search

The semantic search functionality is powered by OpenAI embeddings, which are stored in Pinecone. When a user submits a query, the system retrieves relevant dataset descriptions by comparing the query's semantic embedding with those stored in the database. This process ensures that the most contextually relevant datasets are identified and returned.

### Retrieval Augmented Generation

Once relevant datasets are retrieved, the system uses GPT 4o-turbo to generate explanations of their relevance to the user's query. This step enhances transparency by providing users with insights into why certain datasets were selected.

### Moderation and Hallucination Detection

To ensure the quality and appropriateness of generated content, the system includes moderation and hallucination detection mechanisms. These features help maintain the integrity of the information provided to users by filtering out inappropriate or unsupported content.

### Automated Data Management

Dagster plays a critical role in automating data management tasks. It orchestrates the ingestion, transformation, and indexing of data, ensuring that the Pinecone vector database is always up-to-date. This automation is essential for maintaining the system's performance and accuracy.

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
