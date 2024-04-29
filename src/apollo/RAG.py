from langchain.chains import create_retrieval_chain
from langchain_core.runnables import Runnable

from apollo.Answering import Answering
from apollo.Reformulator import Reformulator


class RAG:
    def __init__(
        self, reformulation_chain: Reformulator, question_answer_chain: Answering
    ):
        self._rag_chain = create_retrieval_chain(
            reformulation_chain, question_answer_chain
        )

    def get_rag_chain(self) -> Runnable:
        return self._rag_chain
