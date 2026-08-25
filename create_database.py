"""
Step 1 of the RAG pipeline: RETRIEVAL SETUP
--------------------------------------------
This script does NOT use any AI generation. It only:
  1. Loads the PDF and extracts raw text
  2. Splits that text into small chunks
  3. Converts each chunk into a vector (embedding) using a FREE local model
  4. Stores those vectors in a local Chroma database on disk

No API key is needed for this step — the embedding model
(all-MiniLM-L6-v2) runs entirely on your own machine.
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os
import shutil

CHROMA_PATH = "chroma"
DATA_PATH = "data/books"


def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    """Load every PDF found in DATA_PATH."""
    all_documents = []
    for filename in os.listdir(DATA_PATH):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(DATA_PATH, filename)
            loader = PyPDFLoader(path)
            all_documents.extend(loader.load())
    print(f"Loaded {len(all_documents)} pages from PDFs in {DATA_PATH}.")
    return all_documents


def split_text(documents):
    """Break long pages into small overlapping chunks for better retrieval."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} pages into {len(chunks)} chunks.")

    # Preview one chunk so you can see what's being stored
    if chunks:
        sample = chunks[min(10, len(chunks) - 1)]
        print("\n--- Sample chunk ---")
        print(sample.page_content)
        print(sample.metadata)
        print("--------------------\n")

    return chunks


def save_to_chroma(chunks):
    # Clear out any old database so we don't mix old and new data.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # This free, local model turns each text chunk into a vector.
    # It downloads once (~90MB) the first time you run this, then it's cached.
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    db = Chroma.from_documents(
        chunks, embedding_function, persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to '{CHROMA_PATH}'.")


if __name__ == "__main__":
    main()