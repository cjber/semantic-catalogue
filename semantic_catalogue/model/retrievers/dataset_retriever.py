from langchain_community.retrievers import PineconeHybridSearchRetriever
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder

from semantic_catalogue.common.settings import cfg


def dataset_retriever():
    bm25_encoder = BM25Encoder().load("bm25/bm25_values.json")
    pc = Pinecone()
    index = pc.Index(cfg.datastore.index_name, host=cfg.datastore.host)
    embeddings = OpenAIEmbeddings(model=cfg.datastore.embed_model)
    return PineconeHybridSearchRetriever(
        embeddings=embeddings,
        sparse_encoder=bm25_encoder,
        index=index,
        top_k=cfg.model.top_k,
        alpha=cfg.model.alpha,
    )
