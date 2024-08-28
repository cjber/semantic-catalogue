---
title: {{Semantic Catalogue}}
emoji: {{emoji}}
colorFrom: {{colorFrom}}
colorTo: {{colorTo}}
sdk: {{docker}}
sdk_version: "{{sdkVersion}}"
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


### Run API

Run the system through an API using:

   ```bash
fastapi run src/search_system/api.py
```

### Run Dagster pipeline

```bash
podman compose up --build -d

```

> WARNING: This is not intended for public use; requires access to a private database.

## Documentation

Further information regarding the methods used may be found in [DOCS.md](./reports/DOCS.md)
