import json
import os
from typing import Any, List

import fitz  # PyMuPDF for extracting PDF text and metadata
import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
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
        embedding_function = embeddings.embed_query
        _DEFAULT = "apollo"
        index_name: str = os.getenv("INDEX_NAME", _DEFAULT)
        fields = [
            SimpleField(
                name="id",
                type=SearchFieldDataType.String,
                key=True,
                filterable=True,
            ),
            SearchableField(
                name="content",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
            SearchField(
                name="content_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=len(embedding_function("Text")),
                vector_search_profile_name="myHnswProfile",
            ),
            SearchableField(
                name="metadata",
                type=SearchFieldDataType.String,
                searchable=True,
            ),
        ]
        vector_store: AzureSearch = AzureSearch(
            azure_search_endpoint=os.getenv("VECTOR_STORE_ADDRESS"),
            azure_search_key=os.getenv("VECTOR_STORE_PASSWORD"),
            index_name=index_name,
            embedding_function=embeddings.embed_query,
            fields=fields,  # This allows us to put any schema we want with Langchain
        )
        search_client: SearchClient = SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=index_name,
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY")),
        )
        self._search_client = search_client
        self._vector_store = vector_store
        self._embedding_function = embedding_function
        self._index_name = index_name
        self._fields = fields

    def get_vector_store(self) -> AzureSearch:
        return self._vector_store

    def get_embedding_function(self) -> Any:
        return self._embedding_function

    def get_index_name(self) -> str:
        return self._index_name

    def get_search_client(self) -> SearchClient:
        return self._search_client

    def get_fields(self) -> List:
        return self._fields

    @staticmethod
    def extract_title(pdf_path: str) -> str:
        title: str = ""
        with fitz.open(pdf_path) as doc:
            title = doc.metadata["title"]  # Attempt to use metadata title
            if not title:  # Fallback to the first line of the first page
                first_page = doc[0]
                title = first_page.get_text().split("\n")[0]
        return title

    @staticmethod
    def load_document(file_path: str) -> List[str]:
        file_type = file_path.split(".")[-1].lower()
        documents = []

        if file_type == "pdf":
            loader = PyPDFLoader(file_path=file_path)
            documents = loader.load()
        elif file_type == "txt":
            loader = TextLoader(file_path)
            documents = loader.load()
        return documents

    def push_document(self, document_path: str, title: str) -> None:
        # Load documents depending on type (PDF or TXT)
        documents = self.load_document(document_path)

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        anonymized_docs = []

        progress_bar = st.progress(0)
        for i, doc in enumerate(docs):
            # Anonymize doc
            # anonymized_doc = Anonymizer(
            #     original_text=doc.page_content
            # ).get_anonymized_text()

            # doc = doc.copy(update={"page_content": anonymized_doc})
            doc.metadata.update(
                {"title": str(title) + "-" + str(i + 1), "source": title}
            )  # This is to ensure that
            # we show different titles for multiple chunks of the same document.
            anonymized_docs.append(doc)
            progress_bar.progress(i + 1)
        progress_bar.empty()

        self._vector_store.add_documents(documents=anonymized_docs)

    def fetch_documents(self, max_results: int = 10) -> List:
        results = []
        results_title = []  # To ensure we don't have duplicates
        search_results = self._search_client.search(search_text="*", top=max_results)
        for result in search_results:
            metadata = json.loads(result["metadata"])
            if metadata["title"] not in results_title:
                results.append(result)
                results_title.append(metadata["title"])

        return results

    def delete_document(self, document_key: str) -> str:
        batch = [{"id": document_key}]
        try:
            self._search_client.delete_documents(documents=batch)
            print(f"Document ID {document_key} deleted.")
            return ""
        except Exception as e:
            return f"Error detected while deleting document {document_key}: {e}"
