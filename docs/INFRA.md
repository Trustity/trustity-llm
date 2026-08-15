# Infrastructure decision — Trustity LLM preview

## Choice

| Layer | Platform | Why |
|-------|----------|-----|
| Chat UI + RAG + specialist FAQ | **Vercel** (`trustitylabs`) | Public site; no GPU; Mac is not in the request path |
| Generative polish | `GROQ_API_KEY` and/or `TRUSTITY_LLM_API_URL` | OpenAI-compatible HTTP; optional |
| Train LoRA | **Mac (MLX)** | Personal machine; train then shut the lid |
| Host fused weights | HF endpoint / VPS / Together — **not the Mac** | Must stay online independently |
| Logging | **Supabase** (optional) | Wire when credentials exist |

## Public URL

- Chat: `https://trustitylabs.com/llm`
- API: `POST /api/llm/ask` `{ "question": "..." }`

## Request path (production)

1. Browser hits Labs on Vercel.
2. Vercel retrieves FAQ + corpus (already in the git repo).
3. If `TRUSTITY_LLM_API_URL` is set, Vercel asks that host to write the answer (your uploaded specialist model).
4. Else if `GROQ_API_KEY` is set, Groq writes the answer from the same RAG context.
5. Else Vercel returns the extractive grounded answer.

The Mac never serves step 3–5.

## Later (Windows 5080)

Use that box as a **trainer** (larger LoRA), still not as the public website runtime unless you deliberately run a server there.
