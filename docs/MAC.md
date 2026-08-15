# Mac path (M-series, 48GB)

Local specialist stack: **FAQ + BM25 RAG**, then **Qwen2.5 Instruct (4-bit MLX)** with an optional **LoRA adapter**.

Public chat on Labs stays on Vercel. This path is for the MacBook, not production hosting.

## Setup

```bash
cd trustity-llm
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-mlx.txt
python3 scripts/build_sft.py
```

## RAG only (no weights)

```bash
python3 scripts/rag_ask.py "What does VisionX detect on an endpoint?"
```

## Generate with base MLX model

First run downloads `mlx-community/Qwen2.5-3B-Instruct-4bit` (~2GB).

```bash
python3 scripts/mlx_ask.py "How does GenGuard reduce GenAI data loss?"
```

On 48GB unified memory you can step up:

```bash
python3 scripts/mlx_ask.py "What is Trustity Axiom used for?" \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit
```

## LoRA (the specialist jump)

```bash
python3 scripts/train_lora_mlx.py --iters 200
python3 scripts/mlx_ask.py "Why rotate local admin passwords with PAM?"
```

`mlx_ask.py` loads `adapters/trustity-mlx` automatically when that folder exists.

Default base for LoRA is **Qwen2.5-3B-Instruct-4bit** so the first train finishes in minutes. Same flags work with the 7B 4-bit id if you want more headroom.

Adapters are gitignored. Do not commit raw weights.

## After this

Larger LoRA (14B) waits for the Windows RTX 5080 unless a 7B run is already good enough on eval questions.
