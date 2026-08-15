# Serving Trustity LLM (not on the Mac, not on Vercel)

Train and fuse on the Mac. Host inference on a machine that can stay online.
Labs (`trustitylabs.com/llm`) only does RAG + an HTTP call.

```
Mac (train) → fused weights / Hugging Face
                    ↓
         always-on inference API
                    ↓
         Vercel TRUSTITY_LLM_API_URL
                    ↓
         https://trustitylabs.com/llm
```

Vercel cannot load Qwen. The personal Mac should not be the public GPU.

## Option A — Hugging Face Inference (simplest upload)

1. `huggingface-cli login`
2. `python3 scripts/export_weights.py --upload-repo Trustity/trustity-llm-qwen3b`
3. Create an Inference Endpoint (or compatible OpenAI-style provider) for that repo.
4. On the Labs Vercel project:

```
TRUSTITY_LLM_API_URL=https://router.huggingface.co/v1/chat/completions
TRUSTITY_LLM_API_KEY=hf_...
TRUSTITY_LLM_MODEL=Trustity/trustity-llm-qwen3b
```

Exact URL depends on the HF product you enable. The Labs route expects an OpenAI chat-completions JSON body.

## Option B — Small always-on VPS (3B 4-bit fits CPU)

Rent a cheap Linux box (Railway / Fly / Hetzner). Run any OpenAI-compatible server in front of the fused weights (vLLM, llama.cpp, TGI). Point `TRUSTITY_LLM_API_URL` at `https://your-host/v1/chat/completions`.

## Option C — Keep Groq for generation

If you do not want to host weights yet: leave `GROQ_API_KEY` on Vercel. The **specialist knowledge is already in the Labs repo** (FAQ cards + corpus). Training on the Mac improves a future hosted model; it is not required for the public `/llm` page to stay useful.

## Env on Labs

See `trustitylabs/.env.example`.
