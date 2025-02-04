<div align="center">

![](./docs/figs/svg/logo-no-background.svg)

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Dagster](https://img.shields.io/badge/Dagster-654FF0?style=for-the-badge&logo=Dagster&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)  
![OpenAI](https://img.shields.io/badge/OpenAI-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![LangChain](https://img.shields.io/badge/langchain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)

---
**The _Semantic Catalogue_ is a project designed to enhance the search capabilities of data catalogues for research purposes. By moving beyond traditional keyword-based searches, it provides users with more accurate and relevant results through semantic understanding.**

---

[Methodology](./reports/DOCS.md) · [View Demo](https://apps.cdrc.ac.uk/semantic-catalogue) · [Getting Started](https://github.com/cjber/semantic-catalogue?tab=readme-ov-file#getting-started)
</div>


## Overview

The Semantic Catalogue is an agentic system designed to enhance the search capabilities of data catalogues by considering semantic understanding. Unlike traditional keyword-based searches, this system uses semantic embeddings to provide users with more accurate and contextually relevant results. The project integrates OpenAI's large language models (LLMs), Pinecone's vector database, and Dagster's data orchestration capabilities, to deliver a comprehensive solution for semantic search and data management.

## Features

- **Semantic Search:** Uses OpenAI embeddings stored in Pinecone to perform semantic queries, enhancing dataset search discoverability over keyword-based solutions.
- **Retrieval Augmented Generation (RAG):** Uses GPT 4o-mini to generate responses that explain the relevance of retrieved datasets, with inline citations, providing transparency and insights.
- **Moderation and Hallucination Detection:** Ensures generated content is appropriate and factually grounded, using moderation and hallucination detection mechanisms.
- **Automated Data Management:** Dagster is used to automate the creation and continuous management of the Pinecone vector database, ensuring efficient data handling and automated updates.

## System Architecture

The Semantic Catalogue uses Retrieval Augmented Generation (RAG), which combines retrieval-based and generation-based LLMs. This involves two main steps:

1. **Retrieval:** Relevant datasets are retrieved based on a user's query using the dot-product similarity semantic embeddings.
2. **Generation:** The retrieved dataset descriptions are used to generate contextually relevant responses that explain their relevance to the query.

![System Architecture](./docs/figs/system.png)
*System Architecture*

- **Backend (FastAPI & LangGraph):** LangGraph provides the core functionality of the system, providing a strucutured framework. FastAPI wraps the graphs, allowing for the system to integrate with external systems.
- **Data Processing (Dagster):** Manages the entire data lifecycle, from ingestion to processing and storage. Dagster ensures that descriptive metadata used in the search system is automatically updated and upserted to a Pinecone database.
- **Vector Database (Pinecone):** Stores semantic embeddings for efficient search operations. Pinecone's vector database is optimised for handling high-dimensional data, making it ideal for semantic search tasks.
- **Machine Learning Models (OpenAI):** Powers the semantic understanding and generation capabilities. OpenAI's models are used to interpret queries and generate relevant responses based on retrieved data.


## Detailed Functionality

### Data Management with Dagster

Dagster automates the data management processes, including data ingestion, transformation, and indexing. This ensures the Pinecone vector database is continuously updated and maintained, which is crucial for the accuracy and relevance of the semantic search capabilities.

![Global Asset Lineage](./docs/figs/Global_Asset_Lineage.svg)
*Global Asset Lineage*


### Semantic Search

The semantic search functionality uses OpenAI embeddings, which are stored in Pinecone. When a user submits a query, the system retrieves relevant dataset descriptions by comparing the query's semantic embedding with those stored in the database. This process ensures that the most contextually relevant datasets are identified and returned.

![Search Graph](./docs/figs/search_graph.png)

### Retrieval Augmented Generation

1. **Generation:** Once relevant datasets are retrieved, the system uses GPT 4o-turbo to generate explanations of their relevance to the user's query. This step enhances transparency by providing users with insights into why certain datasets were selected.

2. **Moderation and Hallucination Detection**: To ensure the quality and appropriateness of generated content, the system includes moderation and hallucination detection mechanisms. These features help maintain the integrity of the information provided to users by filtering out inappropriate generations, or regenerating incorrect dataset summaries.

3. **Automated Data Management**: Dagster automates data management tasks. It orchestrates the ingestion, transformation, and indexing of data, ensuring that the Pinecone vector database is always up-to-date. This ensures that new datasets are automatically embedded and hosted on Pinecone as they are collected by their respective institutions.

![Generation Graph](./docs/figs/gen_graph.png)

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python >=3.12,<3.13
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

    This project uses `uv`:

    ```bash
    uv sync
    ```

    Alternatively, `pip` can also be used to install from a `pyproject.yaml`:

    ```bash
    pip install . # ensure you are using a venv
    ```

4. **Configure the system:**

   Edit the `config/config.toml` file to customise model settings.

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

The Dagster UI is available at `http://localhost:3000`. Adjust the Auto Materialise and Sensor settings to start the automation.
