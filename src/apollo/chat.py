from typing import Any, List, Literal

from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from apollo.Answering import Answering
from apollo.RAG import RAG
from apollo.Reformulator import Reformulator
from apollo.VectorStore import VectorStore

Role = Literal["user", "assistant"]


class Message:
    type: Role
    content: str


class Chat:
    def __init__(self) -> None:
        self.vectorstore = VectorStore()

        # self.vectorstore.push_document("../data/Bilbo_Titan_Mythical_Creature 1.pdf")
        retriever = self.vectorstore.get_vector_store().as_retriever()

        llm = ChatOpenAI(model="gpt-4", temperature=0.1)  # change this

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
