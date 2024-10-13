from langchain_community.document_loaders import TextLoader, Docx2txtLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from PyPDF2 import PdfReader
import re
import os

from SETTINGS import chunk_size


class Splitter:
    def __init__(self, file_name: str):
        self.data_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            add_start_index=True,
            is_separator_regex=False,
            strip_whitespace=True
        )
        self.file_name = file_name

    def clean_files(self) -> list:
        """
        Load and clean file before chunk
        """
        with open(self.file_name, 'rb') as file:
            reader = PdfReader(file)
            extracted_text = []
            for page in reader.pages:
                text = page.extract_text()
                # text = text.split('\n \n \n \n ')[1]
                text = text.strip()
                text_ = text.split(' ')
                text_.pop(0)
                text_ = " ".join(text_)
                extracted_text.append(text_)
            # удаление титульного листа
            del extracted_text[0]
            extracted_text = " ".join(extracted_text)
            pattern = r'(\d+\.\d+\.\d+\.\d+.*?)((?=\n\d+\.\d+\.\d+\.\d+)|$)'
            extracted_text = re.findall(pattern, extracted_text, re.DOTALL)
            extracted_text = [', '.join(map(str, t)) for t in extracted_text]
            documents = self.data_splitter.create_documents(extracted_text)
            documents = self.add_metadata(documents)
            print(f"Total documents: {len(documents)}")
            return documents

    def add_metadata(self, chunk_text):
        """
        Add metadata to chunks
        """
        print(self.file_name)
        file_name_without_extension = (os.path.splitext(self.file_name)[0]).split('/')[1]
        for idx, text in enumerate(chunk_text):
            chunk_text[idx].metadata['metadata'] = {"source": file_name_without_extension}
            return chunk_text

    def process_files(self) -> list | dict:
        """
        Function for split file for chunks (alternative method
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
