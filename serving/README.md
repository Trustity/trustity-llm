# Railway inference (always-on)

The Mac trains. **Railway serves.** Vercel (Labs) only does RAG and then POSTs here.

```
Mac LoRA  →  optional GGUF upload
Railway   →  llama.cpp CPU, OpenAI-compatible /v1/chat/completions
Vercel    →  TRUSTITY_LLM_API_URL=https://<railway>/v1/chat/completions
```

Qwen2.5-3B Q4 fits a Railway instance with **~8GB RAM**. No GPU required. Use a plan that does not sleep if you want the site to answer 24/7.

## Deploy

From the `trustity-llm` repo (this `railway.toml` points the Dockerfile at `serving/`):

1. Create a Railway project, connect GitHub `Trustity/trustity-llm`.
2. Set RAM to 8GB+.
3. Variables:

```
MODEL_REPO=bartowski/Qwen2.5-3B-Instruct-GGUF
MODEL_FILE=Qwen2.5-3B-Instruct-Q4_K_M.gguf
LLM_API_KEY=<long random secret>
N_CTX=2048
```

4. First boot downloads the GGUF (a few minutes). `/health` should return `ok`.
5. Public URL looks like `https://trustity-llm-production.up.railway.app`.

On the **Labs** Vercel project:

```
TRUSTITY_LLM_API_URL=https://<your-railway-host>/v1/chat/completions
TRUSTITY_LLM_API_KEY=<same secret>
TRUSTITY_LLM_MODEL=trustity-llm
```

Leave Groq unset if Railway should be the only generator. If Railway is down, Labs falls back to Groq (if set) or extractive RAG.

## Use the Mac-trained LoRA later

Fuse on the Mac, export GGUF, put it on Hugging Face, then change Railway:

```bash
python3 scripts/export_weights.py --export-gguf
# upload the .gguf to a HF repo you control
```

```
MODEL_REPO=Trustity/trustity-llm-gguf
MODEL_FILE=trustity-qwen3b.Q4_K_M.gguf
```

Until that file exists, Railway serves the public Qwen Instruct GGUF plus Labs RAG — already better than a cold Mac.

## Local smoke test

```bash
cd serving
pip install -r requirements.txt
export LLM_API_KEY=dev
python -m uvicorn server:app --port 8080
curl -s localhost:8080/health
```
