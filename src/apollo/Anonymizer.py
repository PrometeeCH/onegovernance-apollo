import os
from typing import Any

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


class Anonymizer:
    def __init__(self, original_text: str):
        self._original_text = original_text
        llm = ChatOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY_CHAT"), model="gpt-4")
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a specialist in anonymizing documents. When the name of an entity is mentioned,
                       you change it in a simple way.
                       Example: If Goldman Saachs is mentioned, replace it by an american bank.
                       Same for the name of persons etc.""",
                ),
                (
                    "user",
                    "Here's the original document, only return the anonymized document and nothing else. {input}",
                ),
            ]
        )
        chain = prompt | llm
        self._anonymized_text = chain.invoke({"input": self._original_text}).content

    def get_original_text(self) -> str:
        return self._original_text

    def get_anonymized_text(self) -> Any:
        return self._anonymized_text
