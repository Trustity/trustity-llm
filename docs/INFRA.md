# Infrastructure decision — Trustity LLM preview

## Choice

| Layer | Platform | Why |
|-------|----------|-----|
| Chat UI + RAG API | **Vercel** (`trustity-labs`) | Already hosting Labs; Node BM25 is edge/serverless-friendly; one deploy |
| Corpus | Shipped in repo (`data/corpus_chunks_v0.jsonl`) | ~400KB; no DB required for MVP retrieval |
| Generative polish (optional) | Env `GROQ_API_KEY` → open model (Llama/Qwen) | Grounded by RAG; not “naked ChatGPT” |
| Local Mac generative | **MLX** script in `trustity-llm` | Uses M5 unified memory; not for public Vercel |
| Logging / rate metadata | **Supabase** (optional env) | Wire when project credentials available |
| Railway | **Not used for MVP** | No always-on GPU worker needed yet |

## Public URL

- Chat: `/llm` on Labs (`https://trustitylabs.com/llm`)
- API: `POST /api/llm/ask` `{ "question": "..." }`

## Later (Windows 5080)

Move LoRA training + self-hosted inference to the Windows box / Railway GPU if needed; keep Labs UI on Vercel talking to that API.
