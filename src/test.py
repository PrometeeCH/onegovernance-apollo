from typing import List

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src.apollo.Answering import Answering
from src.apollo.RAG import RAG
from src.apollo.Reformulator import Reformulator
from src.apollo.VectorStore import VectorStore

vectorstore = VectorStore()

vectorstore.push_document("../data/Bilbo_Titan_Mythical_Creature 1.pdf")
retriever = vectorstore.get_vector_store().as_retriever()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.1)

reformulation_chain = Reformulator(llm=llm, retriever=retriever).get_history_retriever()
question_answer_chain = Answering(llm=llm).get_qa_chain()
rag_chain = RAG(
    reformulation_chain=reformulation_chain, question_answer_chain=question_answer_chain
)

# example conversation
chat_history: List = []

question = "Who is Bilbo?"

ai_msg_1 = rag_chain.get_rag_chain().invoke(
    {"input": question, "chat_history": chat_history}
)
chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])

second_question = "Tell me more about the first point you said."

output = {}
curr_key = None
for chunk in rag_chain.get_rag_chain().stream(
    {"input": second_question, "chat_history": chat_history}
):
    for key in chunk:
        if key == "answer":
            if key not in output:
                output[key] = chunk[key]
            else:
                output[key] += chunk[key]
            if key != curr_key:
                print(f"\n\n{key}: {chunk[key]}", end="", flush=True)
            else:
                print(chunk[key], end="", flush=True)
            curr_key = key
