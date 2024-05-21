import os
from typing import Any, List, Literal

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import AzureChatOpenAI

from apollo.Answering import Answering
from apollo.RAG import RAG
from apollo.Reformulator import Reformulator
from apollo.VectorStore import VectorStore

load_dotenv()

Role = Literal["user", "assistant"]


class Message:
    type: Role
    content: str


class Chat:
    def __init__(self) -> None:
        self.vectorstore = VectorStore()

        retriever = self.vectorstore.get_vector_store().as_retriever(
            search_type="similarity", search_kwargs={"k": 20}
        )

        llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_CHAT"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY_CHAT"),
        )

        reformulation_chain = Reformulator(
            llm=llm, retriever=retriever
        ).get_history_retriever()

        question_answer_chain = Answering(llm=llm).get_qa_chain()
        self.rag_chain = RAG(
            reformulation_chain=reformulation_chain,
            question_answer_chain=question_answer_chain,
        )
        self.messages: List = []
        self.history: List = []

    def add_message(self, message: str) -> None:
        self.messages.append(HumanMessage(content=message))
        ai_response = self.generate_response(message)
        self.messages.append(AIMessage(content=ai_response))

    def generate_response(self, question: str) -> Any:
        ai_response = self.rag_chain.get_rag_chain().invoke(
            {"input": question, "chat_history": self.messages}
        )
        self.history.extend([HumanMessage(content=question), ai_response["answer"]])
        return ai_response["answer"]
