# Free RAG System (PDF Q&A)

A zero-cost Retrieval-Augmented Generation (RAG) pipeline: ask questions
about any PDF and get answers grounded strictly in that document — no paid
API required.

**Stack:**
- **Chunking + retrieval:** LangChain + Chroma (local vector database)
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2` (free, runs locally, no key needed)
- **Generation:** Groq's free-tier API running `openai/gpt-oss-20b`
- **Mode:** Strict — the model answers only from retrieved PDF content, and
  says so plainly if the answer isn't in the document.

## 1. Install dependencies

```
pip install -r requirements.txt
```

## 2. Get a free Groq API key

1. Go to https://console.groq.com
2. Sign up (no credit card required)
3. Create an API key

## 3. Set up your key

Copy `.env.example` to `.env`:

```
cp .env.example .env
```

Open `.env` and paste your real key — **no quotes, no spaces around the `=`**:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

## 4. Put your PDF in place

Drop your PDF(s) into `data/books/` — the script picks up every `.pdf` file
in that folder.

## 5. Build the vector database

```
python create_database.py
```

This reads the PDF(s), splits the text into chunks, embeds each chunk
locally (free — no internet needed for this step after the embedding model
downloads once, ~90MB), and saves everything into a `chroma/` folder.

Re-running this command wipes and rebuilds `chroma/` from scratch, so it's
safe to re-run any time your source PDFs change.

## 6. Ask questions

```
python query_data.py "Who is Harry Potter's best friend?"
```

This step needs internet (to call Groq) but stays free within Groq's
generous free tier. The retrieved chunks and their similarity scores print
first for transparency, then the final answer prints in **bright green** so
it's easy to spot.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'langchain.text_splitter'`** —
  newer LangChain versions moved this to a separate package. Already fixed
  in this repo's code (`langchain_text_splitters` instead).
- **`Unable to find matching results in the document`** even for obvious
  questions — this was a threshold bug: the old relevance-score cutoff
  (0.5) was tuned for OpenAI's embeddings and doesn't translate to the free
  HuggingFace embedding model's score range. Fixed by switching to raw
  distance scores with no arbitrary cutoff.
- **`groq.NotFoundError: model ... does not exist`** — Groq periodically
  retires models. This repo currently uses `openai/gpt-oss-20b`. If that
  ever gets retired too, check https://console.groq.com/docs/models for
  the current list and update the `model=` line in `query_data.py`.
- **`KeyError: 'GROQ_API_KEY'`** — means `.env` wasn't found or is empty.
  Make sure the file is named exactly `.env` (not `.env.example`), sits in
  the same folder as `query_data.py`, and has no quotes around the key.

## Notes

- The embedding model downloads once, then runs fully offline afterward.
- Every question re-embeds your query and searches the saved database — you
  don't need to rebuild the database between questions, only when your
  source PDFs change.