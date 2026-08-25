# Free RAG System (Harry Potter PDF)

Zero-cost RAG pipeline: local free embeddings + Chroma vector DB + Groq's free Llama 3 for answers.

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

Open `.env` and paste your real key:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

## 4. Put your PDF in place

Your PDF should already be in `data/books/`. To add more PDFs, just drop them
into that same folder — the script picks up every `.pdf` file there.

## 5. Build the vector database

```
python create_database.py
```

This reads the PDF, splits it into chunks, embeds each chunk locally (free,
no internet needed for this step after the model downloads once), and saves
everything into a `chroma/` folder.

## 6. Ask questions

```
python query_data.py "Who is Harry Potter's best friend?"
```

This step needs internet (to call Groq) but is still free within Groq's
generous free tier.

## Notes

- Strict mode is on: answers come only from the PDF's content. If the
  document doesn't cover something, the model will say so instead of
  guessing.
- The embedding model (`all-MiniLM-L6-v2`) downloads once (~90MB) the first
  time you run `create_database.py`, then it's cached locally.
- If you re-run `create_database.py`, it wipes and rebuilds the `chroma/`
  folder from scratch.
