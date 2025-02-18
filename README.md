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

[Methodology](./docs/methods/methods.md) · [View Demo](https://apps.cdrc.ac.uk/semantic-catalogue) · [Getting Started](https://github.com/cjber/semantic-catalogue?tab=readme-ov-file#getting-started)
</div>

## Features

- **Semantic Search:** Leverages OpenAI embeddings in Pinecone for context-aware dataset discovery
- **Retrieval Augmented Generation (RAG):** Generates explanations with inline citations using GPT 4o-mini
- **Content Quality Assurance:** Built-in moderation and hallucination detection
- **Automated Data Pipeline:** Dagster-managed continuous updates to the vector database

## System Architecture

The system uses Retrieval Augmented Generation (RAG) with two core components:

1. **Retrieval:** Finds relevant datasets using semantic similarity
2. **Generation:** Explains dataset relevance using retrieved information

![System Architecture](./docs/figs/system.png)
*System Architecture*

Key components:

- **Backend:** FastAPI & LangGraph for structured processing and API integration
- **Data Pipeline:** Dagster for automated data lifecycle management
- **Vector Database:** Pinecone for efficient semantic search operations
- **AI Models:** OpenAI for semantic understanding and generation

## Detailed Functionality

### Data Management

Dagster automates the entire data pipeline - from ingestion to indexing - ensuring the Pinecone database stays current with new datasets.

![Global Asset Lineage](./docs/figs/Global_Asset_Lineage.svg)

### Search & Generation

1. **Semantic Search:** Queries are converted to embeddings and matched against Pinecone's vector database
2. **RAG Pipeline:** Retrieved datasets are used to generate context-aware explanations
3. **Quality Control:** Moderation and hallucination detection ensure reliable outputs

![Search Graph](./docs/figs/search_graph.png)

![Generation Graph](./docs/figs/gen_graph.png)

### FastAPI Endpoints

FastAPI is used to create a RESTful API allowing for the RAG graphs to interact with external services. The following endpoints are provided:

* **POST Query (`/query`)**: Accepts a search query and returns relevant documents alongside a unique thread ID associated with the query using the LangGraph `search_graph`.
* **GET Explain (`/explain/{thread_id}`)**: Accepts a `thread_id` and `docid` to provide an explanation using the LangGraph `generation_graph`.

### Containerisation

The entire project is containerised using Docker or Podman compose (tested with Podman). The `compose.yml` file gives more detail.

### Project Tree

```bash
semantic_catalogue/  # main project directory
├── common  # shared utility functions and settings
├── datastore  # dagster configuration for data processing
│   ├── assets  # dagster assets (e.g. datafiles)
│   ├── jobs.py  # dagster jobs to combine and automate assets
│   ├── loaders.py  # langchain loaders to create document objects
│   ├── resources.py  # dagster-openai configuration
│   └── schedules.py  # automate creation of assets
├── model  # langgraph functions
│   ├── chains  # chains that use prompts and llms (agents)
│   ├── graph.py  # main graph definitions
│   ├── llms  # openai llm and others if needed
│   ├── logging.py  # basic logging definition
│   ├── main.py  # wraps graphs for external use
│   ├── nodes  # uses chains to define graph nodes
│   ├── retrievers  # contains retrieval code using pinecone
│   └── states.py  # defines graph states
└── search_api  # fastapi code
```

13 directories, 32 files

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python >=3.12,<3.13
- Docker or Podman
- Git

### Development Setup

To develop this project, please follow these steps:

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

To run the project successfully, it expects a `.env` file with the following environment variables defined:

```bash
#!/bin/bash

export CDRC_USERNAME=""
export CDRC_PASSWORD=""
export CDRC_FORM_BUILD_ID=""
export PINECONE_API_KEY=""
export OPENAI_API_KEY=""

# optional
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
export LANGCHAIN_API_KEY=""
export LANGCHAIN_PROJECT=""
```

The `CDRC` environment variables allow you to log in as a normal user, and download the documents. The first two are self-explanatory, but the third is more difficult to find. To obtain the `CDRC_FORM_BUILD_ID`:

1. Go to `https://data.cdrc.ac.uk/user/login`
2. Right click anywhere and choose `inspect` (On Firefox it says **Inspect (Q)**)
3. Click `network` in the inspect window, then type in your username and password and login
4. At the top of the `network` window there should be a 'File' called `login`, select this then click the 'Request' tab.
5. This should show you the `form_build_id` which corresponds with your user, and can be set as an environment variable.

The project is fully containerised using `podman`/`docker` `compose`. To run the full system, execute:

```bash
podman compose up -d
```

### Accessing the Frontend

Once up and running, access the semantic catalogue search at `http://localhost:8001`.

### Running the Dagster Pipeline

The Dagster UI is available at `http://localhost:3000`. Adjust the Auto Materialise and Sensor settings to start the automation.

### Alternative Methods

All scripts run independently, for debugging purposes. For example, to run the full LangGraph pipeline.

```
python -m semantic_catalogue.model.main
```

This submits a test query and print the outputs. Chains also provide outputs for testing:


```bash
python -m semantic_catalogue.model.chains.hallucination
```

This prints the output of a test generation that has hallucinations.


You can also start the API server independently:

```bash
fastapi dev semantic_catalogue/search_api/api.py
```
