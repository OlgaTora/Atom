from langchain_community.document_loaders import TextLoader, Docx2txtLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

from SETTINGS import chunk_size, chunk_overlap


class Splitter:
    def __init__(self, file_name: str):
        self.data_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            # chunk_overlap=chunk_overlap,
            add_start_index=True,
            is_separator_regex=False,
            strip_whitespace=True
        )
        self.file_name = file_name

    def process_files(self) -> list | dict:
        """
        Function for split file for chunks
        """
        documents = []
        if self.file_name.endswith('.docx'):
            loader = Docx2txtLoader(self.file_name)
        elif self.file_name.endswith('.txt'):
            loader = TextLoader(self.file_name)
        elif self.file_name.endswith('.pdf'):
            loader = PyPDFLoader(self.file_name)
        else:
            return {"message": "Only txt, docx and pdf files are supported"}
        print(f'file {self.file_name} load')
        text_data = loader.load()
        documents += self.data_splitter.split_documents(text_data)
        print(f"Total documents: {len(documents)}")
        return documents
