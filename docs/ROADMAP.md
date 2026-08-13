# Roadmap

## Phase 0 — Foundation (current)

- [x] Repo + charter
- [ ] Confirm compute / language / Trustity-docs policy (blocking questions to Tal)
- [ ] Freeze base-model shortlist
- [ ] Seed eval suite v0 (50–100 Qs)
- [ ] Data policy + source list

**Exit:** we can start collecting/generating training data without re-litigating product scope.

## Phase 1 — RAG MVP (public value fast)

- Build curated public security corpus (markdown/JSONL)
- Simple retrieval + grounded answers (API)
- Thin chat UI on Labs (“Trustity LLM — preview”)
- Measure: faithfulness + on-topic rate

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
