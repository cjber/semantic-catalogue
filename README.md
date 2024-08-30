---
title: Semantic Catalogue
colorFrom: red
colorTo: gray
sdk: docker
app_file: src/search_api/api.py
pinned: false
---

# Semantic Catalogue

## Overview

The Semantic Search Catalogue is a project designed to enhance the search capabilities of a collection of data catalogues for research. The goal is to move beyond traditional keyword-based searches, providing users with more accurate and relevant results.

## Features

- **Semantic Search:** Embeds documents using OpenAI which are stored on Pinecone, allowing for semantic querying using cosine similarity.

- **Retrieval Augmented Generation:** Generates responses using GPT 3.5 turbo to explain the relevance of retrieved datasets.

## System Architecture

The Semantic Catalogue follows a standard Retrieval Augmented Generation (RAG) architecture:

![](./reports/figs/system.png)

Dagster is used to automate the creation of the Pinecone vector database:

![](./reports/figs/Global_Asset_Lineage.svg)

## Build Python environment

To contribute, please follow the instructions below:

1. Clone the repository:

   ```bash
    git clone https://github.com/cjber/semantic-catalogue.git
   ```

2. Install dependencies:

    ```bash
    cd cdrc-semantic-search
    pip install -r requirements.lock
    ```

3. Configure the system:

Edit the `config/config.toml` file to customise model settings.

## Run Project

The project is fully containerised using `podman`/`docker` `compose`. To run the full system execute:

```bash
podman compose up -d
```

### Semantic Catalogue Search

Once up and running, the semantic catalogue search may be accessed at `localhost:8001`.

### Run Dagster pipeline

The Dagster UI is available at `localhost:3000`. You will need to adjust the Auto Materialize and Sensor settings to start the automation.


> WARNING: This project is not intended for public use; requires access to a private database.

## Documentation

Further information regarding the methods used may be found in [DOCS.md](./reports/DOCS.md)
