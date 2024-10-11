import os
from typing import Any
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS

from SETTINGS import DB_PATH, MODEL


class VectorStore:

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=MODEL)

    def load_vectordb(self):
        db = FAISS.load_local(DB_PATH, self.embeddings, allow_dangerous_deserialization=True)
        return db

    def add_2vectordb(self, documents: Any):
        db = FAISS.from_documents(documents, self.embeddings)
        if os.path.exists(DB_PATH):
            local_index = self.load_vectordb()
            local_index.merge_from(db)
            local_index.save_local(DB_PATH)
        else:
            db.save_local(DB_PATH)

