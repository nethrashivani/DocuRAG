````markdown
# Document RAG Q&A System

A Retrieval-Augmented Generation (RAG) system that allows users to use their own PDF documents, create a searchable vector database from their content, and ask questions based on the information contained in those documents.

The system processes PDF documents, splits them into smaller chunks, generates vector embeddings, stores them in ChromaDB, retrieves the most relevant content for a user query, and uses an LLM to generate a context-grounded answer.

The project is document-agnostic and can be used with different PDFs without changing the application code.

## Features

- Supports single or multiple PDF documents
- Allows users to replace the sample document with their own PDFs
- Automatic document text extraction
- Document chunking with overlapping sections
- Local semantic embeddings using Hugging Face
- Local vector storage using ChromaDB
- Similarity-based document retrieval
- LLM-powered question answering using Groq
- Context-grounded responses
- Prevents the model from relying on information outside the retrieved document context
- Rebuilds the vector database whenever documents are changed

## Tech Stack

- **Language:** Python
- **RAG Framework:** LangChain
- **Document Processing:** PyPDF
- **Embeddings:** Hugging Face `all-MiniLM-L6-v2`
- **Vector Database:** ChromaDB
- **LLM:** Groq `openai/gpt-oss-20b`
- **Environment Management:** python-dotenv

## Project Structure

```text
document-rag/
│
├── data/
│   └── books/
│       └── *.pdf
│
├── chroma/
│
├── create_database.py
├── query_data.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
````

## How It Works

The application follows a standard Retrieval-Augmented Generation pipeline:

```text
PDF Documents
      ↓
Text Extraction
      ↓
Document Chunking
      ↓
Embedding Generation
      ↓
ChromaDB
      ↓
User Query
      ↓
Similarity Search
      ↓
Relevant Document Chunks
      ↓
Groq LLM
      ↓
Context-Grounded Answer
```

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/nethrashivani/hogwarts-rag.git
cd hogwarts-rag
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Groq API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

The API key is used to access the Groq-hosted LLM for answer generation.

Make sure the `.env` file is not committed to the repository.

### 4. Add Your Own PDF Documents

The project is **not limited to the sample Harry Potter document**.

You can use the system with your own PDF documents by placing them inside:

```text
data/books/
```

For example:

```text
data/books/
├── machine-learning.pdf
├── research-paper.pdf
└── python-notes.pdf
```

You can use:

* Books
* Research papers
* Academic notes
* Technical documentation
* Reports
* Manuals
* Project documentation
* Other text-based PDF documents

The system automatically processes all PDF files present in the directory.

No changes to the Python code are required when switching to different documents.

### 5. Create the Vector Database

After adding your documents, run:

```bash
python create_database.py
```

This step:

1. Reads the PDF documents from `data/books/`
2. Extracts their text
3. Splits the text into smaller overlapping chunks
4. Generates embeddings for each chunk
5. Stores the embeddings in ChromaDB

The resulting vector database is stored in:

```text
chroma/
```

Whenever you add, remove, or replace PDF documents, run `create_database.py` again to rebuild the vector database using the updated documents.

### 6. Query Your Documents

Once the vector database has been created, ask questions using:

```bash
python query_data.py "Your question about the document"
```

For example:

```bash
python query_data.py "What is this document about?"
```

Or:

```bash
python query_data.py "What are the main concepts discussed in the document?"
```

The system retrieves the most relevant sections from your documents and uses them as context for generating the answer.

## Example

The repository may contain a sample Harry Potter PDF, but it is only used as example data.

For example:

```bash
python query_data.py "Who is Harry Potter's best friend?"
```

If you replace the sample PDF with a machine learning textbook, you can instead ask:

```bash
python query_data.py "What is supervised learning?"
```

If you replace it with a research paper, you can ask questions about that paper:

```bash
python query_data.py "What methodology was used in the study?"
```

The same RAG pipeline works with each document.

## Using Different Documents

To use a completely different set of documents:

```text
1. Remove or replace the existing PDFs
          ↓
2. Add your own PDFs to data/books/
          ↓
3. Run create_database.py
          ↓
4. Documents are chunked
          ↓
5. New embeddings are generated
          ↓
6. ChromaDB is rebuilt
          ↓
7. Ask questions using query_data.py
```

For example:

```text
data/books/
├── company-handbook.pdf
├── employee-guide.pdf
└── policies.pdf
```

Then:

```bash
python create_database.py
```

After the database is rebuilt:

```bash
python query_data.py "What is the leave policy?"
```

No changes to the application code are required.

## RAG Implementation

### Document Processing

PDF documents are loaded using PyPDF and converted into text.

The extracted content is then divided into smaller overlapping chunks using LangChain's text splitter.

### Embedding Generation

Each document chunk is converted into a numerical vector representation using:

```text
all-MiniLM-L6-v2
```

The embedding model runs locally, so document embeddings do not require a paid embedding API.

### Vector Storage

The generated embeddings and document chunks are stored locally using ChromaDB.

### Retrieval

When a user submits a question, the query is converted into an embedding and compared against the stored document embeddings.

The most relevant document chunks are retrieved using similarity search.

### Response Generation

The retrieved chunks are provided to the Groq-hosted LLM as context along with the user's question.

The model is instructed to answer using the retrieved document context and avoid generating information that is not supported by the available content.

## Context-Grounded Responses

The system is designed to keep answers grounded in the retrieved document content.

If the retrieved information does not contain enough information to answer a question, the model is instructed to indicate that the answer cannot be determined from the available document context rather than relying on outside knowledge.

## Updating Documents

Whenever the source PDFs change, rebuild the vector database:

```bash
python create_database.py
```

The existing ChromaDB data is cleared and rebuilt using the current PDFs in:

```text
data/books/
```

You do not need to rebuild the database for every question.

The database only needs to be rebuilt when the source documents change.

## Environment Variables

| Variable       | Description                    |
| -------------- | ------------------------------ |
| `GROQ_API_KEY` | API key used for LLM inference |

## Requirements

* Python 3.11+
* Internet connection for Groq API requests
* Groq API key
* One or more text-based PDF documents

The embedding model runs locally after its initial download.

## Future Improvements

* Web-based user interface
* Drag-and-drop document uploads
* Conversation history
* Source citations
* Streaming responses
* Document-specific filtering
* Metadata-aware retrieval
* RAG evaluation using RAGAS or DeepEval
* Docker support

## Author

**Nethrashivani**

GitHub: [https://github.com/nethrashivani](https://github.com/nethrashivani)

```
