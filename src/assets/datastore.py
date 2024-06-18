from dagster import AssetExecutionContext, asset
from dagster_openai import OpenAIResource
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

from src.common.utils import Consts, Paths

load_dotenv()


@asset(compute_kind="Pinecone")
def pinecone_index(context: AssetExecutionContext):
    pc = Pinecone()
    if Consts.INDEX_NAME in [index["name"] for index in pc.list_indexes()]:
        pc.delete_index(Consts.INDEX_NAME)

    pc.create_index(
        name=Consts.INDEX_NAME,
        dimension=Consts.EMBEDDING_DIM,
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        metric="cosine",
    )


@asset(compute_kind="OpenAI", deps=["adr_descriptions", "pinecone_index"])
def adr_pinecone(context: AssetExecutionContext, openai: OpenAIResource):
    loader = DirectoryLoader(
        Paths.ADR / "descriptions",
        glob="*.txt",
        loader_cls=TextLoader,
        use_multithreading=True,
        show_progress=True,
    )
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    with openai.get_client(context) as client:
        embeddings = OpenAIEmbeddings(
            client=client.embeddings,
            model=Consts.EMBEDDING_MODEL,
        )

    PineconeVectorStore.from_documents(docs, embeddings, index_name=Consts.INDEX_NAME)
