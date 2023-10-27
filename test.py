from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter

def load_doc(file):
    from langchain.document_loaders import PyPDFLoader
    loader=PyPiDFLoader(file)
    pages  = loader.load_and_split()
    #print("pages",pages)
    return loader.load()

alternative_path = '/Users/jcopps/Downloads/LLM_-_TMDB_-_Conversation_Services.pdf'
actual_path = 'WO2022182409.pdf'
#content = load_doc(actual_path)
content = UnstructuredPDFLoader(actual_path)
content = content.load()
#print(content)
#for page in content:
#    print(page)


"""
loaded_data = []
loaded_data.extend(loader.load())
print("Length: ", len(loaded_data))
def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=10)
documents = text_splitter.split_documents(loaded_data)
print(len(documents))
"""
