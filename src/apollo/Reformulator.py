from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI


class Reformulator:
    def __init__(self, llm: ChatOpenAI, retriever: VectorStoreRetriever) -> None:
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        # Create a chain that takes conversation history and returns documents
        self._history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )

    def get_history_retriever(self) -> Runnable:
        return self._history_aware_retriever
