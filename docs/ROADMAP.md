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

## Phase 2 — Specialist weights (Mac first)

- [x] SFT mix v0 from FAQ + refuse/off-topic pairs (`scripts/build_sft.py`)
- [x] MLX LoRA recipe on Apple Silicon (`docs/MAC.md`, `scripts/train_lora_mlx.py`)
- [x] Run LoRA on the M5 (3B 4-bit default; 7B optional)
- [ ] Score eval suite vs base + adapter
- [ ] LoRA 14B on Windows RTX 5080 when that box is the trainer
- [ ] Push to Hugging Face (gated default)

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
