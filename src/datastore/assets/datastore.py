import time
from pathlib import Path

from dagster import (
    AssetExecutionContext,
    AutoMaterializePolicy,
    AutoMaterializeRule,
    asset,
)
from dagster_openai import OpenAIResource
from langchain_community.document_loaders import DirectoryLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from src.common.settings import cfg
from src.common.utils import Paths
from src.datastore.loaders import ADRLoader, CDRCLoader, UKDSLoader

wait_on_all_parents_policy = AutoMaterializePolicy.eager().with_rules(
    AutoMaterializeRule.skip_on_not_all_parents_updated()
)


def _process_documents(
    context: AssetExecutionContext,
    openai: OpenAIResource,
    paths: list[Path],
    glob_patterns: list[str],
    loader_classes: list[type],
):
    documents = []
    for path, glob_pattern, loader_cls in zip(paths, glob_patterns, loader_classes):
        loader = DirectoryLoader(
            str(path),
            glob=glob_pattern,
            loader_cls=loader_cls,
            use_multithreading=True,
            show_progress=True,
        )
        documents.extend(loader.load())

    with openai.get_client(context) as client:
        embeddings = OpenAIEmbeddings(
            client=client.embeddings, model=cfg.datastore.embed_model
        )

    text_splitter = SemanticChunker(
        embeddings=embeddings, breakpoint_threshold_type="percentile"
    )
    docs = text_splitter.split_documents(documents)

    vectorstore = PineconeVectorStore(
        index_name=cfg.datastore.index_name, embedding=embeddings
    )
    vectorstore.add_documents(documents=docs)


@asset(
    compute_kind="Pinecone",
    deps=["adr_descriptions", "ukds_abstracts", "cdrc_notes", "cdrc_pdfs"],
    auto_materialize_policy=wait_on_all_parents_policy,
)
def pinecone_index(context: AssetExecutionContext, openai: OpenAIResource):
    pc = Pinecone()
    if cfg.datastore.index_name in [index["name"] for index in pc.list_indexes()]:
        pc.delete_index(cfg.datastore.index_name)

    pc.create_index(
        name=cfg.datastore.index_name,
        dimension=cfg.datastore.embed_dim,
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        metric="cosine",
    )
    while not pc.describe_index(cfg.datastore.index_name).status["ready"]:
        time.sleep(1)

    _process_documents(
        context,
        openai,
        paths=[Paths.ADR / "txt"],
        glob_patterns=["*.txt"],
        loader_classes=[ADRLoader],
    )
    _process_documents(
        context,
        openai,
        paths=[Paths.CDRC / "txt", Paths.CDRC / "pdf"],
        glob_patterns=["*.txt", "*.pdf"],
        loader_classes=[CDRCLoader, CDRCLoader],
    )
    _process_documents(
        context,
        openai,
        paths=[Paths.UKDS / "txt"],
        loader_classes=[UKDSLoader],
        glob_patterns=["*.txt"],
    )
