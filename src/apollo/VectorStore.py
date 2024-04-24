import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()


class VectorStore:
    def __init__(self) -> None:
        embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv("AZURE_DEPLOYMENT"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        index_name: str = "apollo-test-index-from-code"
        vector_store: AzureSearch = AzureSearch(
            azure_search_endpoint=os.getenv("VECTOR_STORE_ADDRESS"),
            azure_search_key=os.getenv("VECTOR_STORE_PASSWORD"),
            index_name=os.getenv("INDEX_NAME"),
            embedding_function=embeddings.embed_query,
        )

        self._vector_store = vector_store
        self._embedding_function = embeddings
        self._index_name = index_name

    def get_vector_store(self) -> AzureSearch:
        return self._vector_store

    def get_embedding_function(self) -> AzureOpenAIEmbeddings:
        return self._embedding_function

    def get_index_name(self) -> str:
        return self._index_name

    def push_document(self, document_path: str) -> None:
        loader = PyPDFLoader(document_path)

        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        self._vector_store.add_documents(documents=docs)
