from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_openai import AzureChatOpenAI


class Answering:
    def __init__(self, llm: AzureChatOpenAI):
        qa_system_prompt = """You are an assistant specialized in commodity trading. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer, use chatGPT general knowledge. \
        Give as much answer as possible but still keep the answer concise. \

        {context}"""

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        self._question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    def get_qa_chain(self) -> Runnable:
        return self._question_answer_chain
