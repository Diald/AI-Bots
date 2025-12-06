from openai import OpenAI
from pypdf import PdfReader
import chromadb

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"                       # dummy value required by SDK
)

chroma_client = chromadb.Client()
collections = chroma_client.create_collection("pdf_chunks")


def load_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def embed_text(text):
    response = client.embeddings.create(
        model="nomic-embed-text",          # works in Ollama for embeddings
        input=text
    )
    return response.data[0].embedding


def chunk_text(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def build_vector_db(path):
    text = load_pdf(path)
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        collections.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk]
        )


def ask(query):
    query_embedding = embed_text(query)

    result = collections.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    context = "\n".join(result["documents"][0])

    response = client.chat.completions.create(
        model="llama2:7b",                 # ✅ use smaller model to avoid GPU/RAM error
        messages=[
            {"role": "system", "content": "Answer using the context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )

    return response.choices[0].message["content"]


pdf_path = input("Enter the path of PDF: ")
build_vector_db(pdf_path)

while True:
    q = input("\nAsk something about the PDF: ")
    print("\nAnswer:", ask(q))