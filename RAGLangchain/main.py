import os 
from pathlib import Path 
from pypdf import PdfReader
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter #splits the text
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chains import RetrievalQA
from langchain_groq import ChatGroq

load_dotenv()

DOCS_DIR = Path('docs')
PERSIST_DIR = "chroma_db"
CHUNK_SIZE = 800 # 800 characters will be converted into one embedding
CHUNK_OVERLAP = 200 # each chunk overlaps with previous chunk by 200 characters so that 
# nothing is left mid sentence 
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_pdfs_and_txts(directory: Path):
    '''loading all pdfs and texts under directory and return list of langchain documents'''
    docs = []
    for p in directory.glob("**/*"):
        if p.suffix.lower()==".pdf":
            text = ""
            try: 
                reader = PdfReader(str(p))
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            except Exception as e:
                print(f"failed to load pdf {p}:{e}")
                continue
            from langchain.schema import Document 
            docs.append(Document(page_content=text, metadata={"source": str(p)})) #
        elif p.suffix.lower() in [".txt", ".md"]:
            with open(p, "r", encoding="utf-8") as f:
                text = f.read()
            from langchain.schema import Document 
            docs.append(Document(page_content=text, metadata={"source": str(p)}))
    return docs


def chunk_documents(documents):
    ''' it takes full document and convert it into smaller chunks in the langchain 
    Document object'''
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE, 
        chunk_overlap = CHUNK_OVERLAP, 
        length_function = len
    )
    chunked_docs = []
    for doc in documents:
        splits = text_splitter.split_text(doc.page_content)
        for i, s in enumerate(splits):
            from langchain.schema import Document
            chunked_docs.append(Document(page_content = s, metadata = {**doc.metadata, "chunk": i}))
    return chunked_docs


def build_vectorStore(documents, persistent_dir= PERSIST_DIR, embedding_model = EMBEDDING_MODEL):
    '''create / load a chroma vectorstore from documents'''
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    if not os.path.exists(persistent_dir) or not os.listdir(persistent_dir):
        print("creating new chroma DB and adding documents...")
        vectordb = Chroma.from_documents(
            documents, 
            embeddings, 
            persist_directory = persistent_dir
        )
        vectordb.persist()
    else:
        print("loading existing chroma DB...")
        vectordb = Chroma(
            persist_directory = persistent_dir, 
            embedding_function = embeddings
        )
    return vectordb

def qa_retriever_chain(vectordb, llm=None, k=4):
    '''retrieval QA is a langchain component that takes input question, retrieves most relevant
    data from the document, sends both i/p question and retrieved chunks to llm and gets a response'''
    retriever = vectordb.as_retriever(search_kwargs={"k":k}) #The retriever will return the top k
    #most similar chunks
    llm = ChatGroq(model="llama3-8b", temperature = 0)
        
    qa = RetrievalQA.from_chain_type(
        llm=llm, 
        retriever=retriever, 
        chain_type="stuff") #take all the
    # retrieval chunks and stuff them directly into one single prompt
    return qa

def interactive_loop(qa_chain):
    print("\nRAG chain ready, type 'exit' to exit")
    while True:
        q = input("\n ask a question")
        if q.strip().lower() in ["exit", "quit"]:
            break 
        res = qa_chain.run(q)
        print("\n response- \n")
        print(res)
        
def main():
    print("Loading documents...")
    docs = load_pdfs_and_txts(DOCS_DIR)
    if not docs:
        print("No documents found in docs/ — add PDFs or text files and rerun.")
        return

    print(f"Loaded {len(docs)} documents. Chunking...")
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks. Building vector store...")

    vectordb = build_vectorStore(chunks)
    print("Vector store ready.")

    print("Building QA chain...")
    # If you want to pass a local LLM wrapper, create 'llm' and pass to build_qa_chain
    qa_chain = qa_retriever_chain(vectordb)
    interactive_loop(qa_chain)


if __name__ == "__main__":
    main()