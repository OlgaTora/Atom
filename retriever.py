# from langchain.retrievers import EnsembleRetriever
# from langchain_community.retrievers import BM25Retriever
import SETTINGS
from vector_store import VectorStore


class Retriever:
    def __init__(self, documents):
        self.documents = documents
        self.bm25_coef = SETTINGS.bm25_coef
        self.similarity_coef = SETTINGS.similarity_coef

    def get_vector_retriever(self):
        db = VectorStore().load_vectordb()
        vector_retriever = db.as_retriever(
            search_type='similarity', search_kwargs={'k': self.similarity_coef}
        )
        return vector_retriever

    def get_keyword_retriever(self):
        keyword_retriever = BM25Retriever.from_documents(self.documents)
        keyword_retriever.k = self.bm25_coef
        return keyword_retriever

    def get_ensemble_retriever(self):
        vector_retriever = self.get_vector_retriever()
        keyword_retriever = self.get_keyword_retriever()
        # ensemble_retriever = EnsembleRetriever(
        #     retrievers=[keyword_retriever, vector_retriever],
        #     weights=[0.3, 0.7]
        # )
        # return ensemble_retriever