# Roadmap

## Phase 0 — Foundation (current)

- [x] Repo + charter
- [x] Confirm compute / language / Trustity-docs policy
- [x] Lock decisions (`docs/DECISIONS.md`)
- [x] Seed eval suite v0
- [x] Ingest trustity.co + local trustity.dev docs → corpus v0 (390 chunks)
- [x] Mac-friendly RAG preview script (`scripts/rag_ask.py`)

**Exit:** ready for Phase 1 grounded demo wiring into Labs.

## Phase 1 — RAG MVP (in progress)

- [x] Package retrieval for Labs (`/api/llm/ask` + BM25)
- [x] Chat UI on Labs (`/llm`)
- [x] Optional Groq generative polish via env
- [x] Local MLX script (`scripts/mlx_ask.py`)
- [x] Infra decision doc (`docs/INFRA.md`)
- [ ] Supabase logging (SQL ready; needs project credentials)
- [x] Curated specialist FAQ cards + query expansion + insufficient-context path
- [x] Measure faithfulness on eval suite (`npm run eval:llm` in Labs)

**Exit:** public preview that already feels more niche-correct than raw ChatGPT for our eval prompts.

## Phase 2 — Specialist weights

- Choose base (default proposal: **Qwen2.5-14B-Instruct** or **Llama-3.1-8B-Instruct** if GPU-tight)
- Build SFT mix: seed Q&A + synthetic (teacher-filtered) + refused/unsafe pairs
- LoRA fine-tune + merge optional
- Publish eval scores vs base
- Push to Hugging Face (public or gated)

**Exit:** downloadable / hostable specialist model with documented eval.

## Phase 3 — Productionize demo

- Rate limits, abuse monitoring, logging redaction
- Labs Request Access + HF card
- Optional Hebrew pack
- Continuous eval in CI

## Non-roadmap (explicitly deferred)

- Training a foundation model from scratch
- Agent that executes attacks
- Deep integration with customer tenant data
