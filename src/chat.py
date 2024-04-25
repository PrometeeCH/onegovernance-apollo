import sys
from typing import List, Literal

from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
sys.path.append("/Users/george/Desktop/prometee/apollo")
from src.apollo.Answering import Answering
from src.apollo.RAG import RAG
from src.apollo.Reformulator import Reformulator
from src.apollo.VectorStore import VectorStore


Role = Literal["user", "assistant"]
class Message:
    type: Role
    content: str


class Chat:
    def __init__(self) -> None:
        self.vectorstore = VectorStore()

        #self.vectorstore.push_document("../data/Bilbo_Titan_Mythical_Creature 1.pdf")
        retriever = self.vectorstore.get_vector_store().as_retriever()

        llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.1) #change this

        reformulation_chain = Reformulator(llm=llm, retriever=retriever).get_history_retriever()
        question_answer_chain = Answering(llm=llm).get_qa_chain()
        self.rag_chain = RAG(
            reformulation_chain=reformulation_chain, question_answer_chain=question_answer_chain
        )
        self.messages: List = []
    
    def add_message(self, message: str) -> None:

        self.messages.append(HumanMessage(content=message))

        ai_response = self.generate_response(message)
        #print(ai_response)
        self.messages.append(AIMessage(content=ai_response))


    def generate_response(self, question: str) -> str:
        ai_response = self.rag_chain.get_rag_chain().invoke(
            {"input": question, "chat_history": self.messages}
        )
        #print(ai_response)
        return ai_response["answer"]
    
    

