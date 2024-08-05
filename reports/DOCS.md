# Introduction

* Unify search across catalogues
* Uses semantic search with RAG for results explainability
* LangGraph/LangChain framework

# Methodology

## Pre-processing

For each catalogue their respective API was used to return dataset metadata. Each returned result contained descriptive information regarding datasets, which form the bulk of text data used by the semantic search system to return results. For the CDRC catalogue, PDFs were also processed to extract text. Other metadata was also returned which may be used by the final system; for example, data creation date.

## Datastore

The description of each dataset were then saved into individual text files, identifiable by a unique ID. These files were then embedded using OpenAI embeddings, and uploaded to the Pinecone database, alongside any metadata. Descriptions were 'chunked' into individual segments 1024 tokens in length. For each chunk, the dataset title as embedded at the start.

## RAG Model

A RAG system was then built which embeds a user query using the same embedding model, and returns the top 'k' results ranked by cosine similarity from the Pinecone database. To ensure that results are ranked by dataset, a custom document grouping postprocessor was defined, which grouped all document chunks relating to the same dataset. The highest score from any chunk is used to rank grouped documents.

An adjustable 'alpha' value was used to allow for a mixture of traditional 'sparse vector' search (e.g. BM25: keyword search), and the 'dense vector' search, using the LLM embeddings.

For each unique document returned, an explainable 'Ask AI' option was added, which feeds the grouped document into a GPT LLM with the following prompt:

```python
prompt = """
A user has queried a data catalogue, which has returned a relevant dataset.

Explain the relevance of this dataset to the query in under three sentences. Use your own knowledge or the data profile. Do not say it is unrelated; attempt to find a relevant connection.

Query: "{query}"

Dataset description:

{context}
"""
```

This approach ensures that users receive not only relevant search results but also understandable explanations regarding the relevance of each dataset to their query.

# System architecture

## Overview

![]('./figs/system.png')

## Data flow

(Describe the flow of data from the catalogues to the end-user.)

## Implementation details

* Tools and Libraries: OpenAI API, Pinecone, Llama Index
* Challenges: (Detail any challenges and solutions.)

# Evaluation and results

* Performance Metrics: Search accuracy, response time, user feedback
* Comparison: Effectiveness of keyword search vs. dense vector search

# Future work and improvements

* Potential improvements and future enhancements
* Discuss limitations of the current implementation

# Conclusion

Summarise the key points and the impact of the unified search system.
References

(List any academic papers, tools, or libraries referenced.)
