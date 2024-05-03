from typing import List

from langchain_openai import ChatOpenAI

from src.apollo.Answering import Answering
from src.apollo.RAG import RAG
from src.apollo.Reformulator import Reformulator
from src.apollo.VectorStore import VectorStore

vectorstore = VectorStore()

retriever = vectorstore.get_vector_store().as_retriever(k=20)

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.1)

reformulation_chain = Reformulator(llm=llm, retriever=retriever).get_history_retriever()
question_answer_chain = Answering(llm=llm).get_qa_chain()
rag_chain = RAG(
    reformulation_chain=reformulation_chain, question_answer_chain=question_answer_chain
)

# example conversation
chat_history: List = []

question = "Quelle est la date de faillite de la banque Lehman Brothers?"

ai_msg_1 = rag_chain.get_rag_chain().invoke(
    {"input": question, "chat_history": chat_history}
)

print(ai_msg_1["answer"])
# chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])
