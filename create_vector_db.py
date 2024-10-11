from SETTINGS import FILES_DIR
from files_list import FileNamesLoader
from splitter import Splitter
from vector_store import VectorStore

files_to_split = FileNamesLoader(FILES_DIR).get_files_list()
documents = Splitter(files_to_split).process_files()
db = VectorStore().add_2vectordb(documents)
print('Create Vector Store "db_bot_qdrant"')

# SOZDAT PAPKU STORAGE!!