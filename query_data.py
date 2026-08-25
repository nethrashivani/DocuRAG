"""
Step 2 of the RAG pipeline: RETRIEVAL + GENERATION
----------------------------------------------------
This is where an actual AI model gets involved.

1. Your question gets embedded with the SAME free local model
   used to build the database (must match, or the vectors won't compare correctly).
2. Chroma finds the most relevant chunks from the PDF.
3. Those chunks + your question are sent to Groq's free hosted
   Llama 3 model, which reads them and writes a real answer.

STRICT MODE: the prompt tells the model to answer ONLY using the
retrieved chunks. If the PDF doesn't contain the answer, it will
say so instead of guessing or using outside knowledge.

You need a free Groq API key for this step: https://console.groq.com
"""

import argparse
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from colorama import init, Fore, Style

# colorama makes ANSI color codes work properly in Windows terminals too.
init(autoreset=True)

load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context. If the context
does not contain enough information to answer, say so clearly instead
of guessing or using outside knowledge.

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The question to ask.")
    args = parser.parse_args()
    query_text = args.query_text

    # Must use the same embedding model that built the database.
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Retrieval: find the most relevant chunks for this question.
    # NOTE: we use raw similarity_search_with_score (distance-based) instead of
    # similarity_search_with_relevance_scores, because that method's 0-1
    # "relevance" normalization assumes OpenAI-style embeddings. With the free
    # HuggingFace embedding model, its scores land on a different scale and
    # a fixed 0.5 cutoff can wrongly discard good matches.
    results = db.similarity_search_with_score(query_text, k=3)

    print("\n--- Retrieved chunks (lower distance = more relevant) ---")
    for doc, score in results:
        print(f"[distance={score:.4f}] {doc.page_content[:80]}...")
    print("-----------------------------------------------------------\n")

    if len(results) == 0:
        print("Unable to find matching results in the document.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Generation: send retrieved chunks + question to Groq's free hosted model.
    model = ChatGroq(model="openai/gpt-oss-20b", api_key=os.environ["GROQ_API_KEY"])
    response = model.invoke(prompt)

    sources = [doc.metadata.get("source", "unknown") for doc, _score in results]

    # Print the final answer in bright green so it stands out from the
    # retrieval/debug logs above it.
    print(Fore.GREEN + Style.BRIGHT + "\n=========== ANSWER ===========")
    print(Fore.GREEN + Style.BRIGHT + response.content)
    print(Fore.GREEN + Style.BRIGHT + "===============================\n")

    print(Fore.CYAN + f"Sources: {sources}")


if __name__ == "__main__":
    main()