# Roadmap

## Phase 0 — Foundation (current)

- [x] Repo + charter
- [x] Confirm compute / language / Trustity-docs policy
- [x] Lock decisions (`docs/DECISIONS.md`)
- [x] Seed eval suite v0
- [x] Ingest trustity.co + local trustity.dev docs → corpus v0 (390 chunks)
- [x] Mac-friendly RAG preview script (`scripts/rag_ask.py`)

**Exit:** ready for Phase 1 grounded demo wiring into Labs.

## Phase 1 — RAG MVP (next)

- [ ] Package retrieval as tiny API
- [ ] Optional: local MLX 3B/7B to *generate* from retrieved context on the Mac
- [ ] Thin chat UI on Labs (“Trustity LLM — preview”)
- [ ] Measure: faithfulness + on-topic rate on eval suite

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
