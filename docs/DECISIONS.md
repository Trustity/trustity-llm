# Locked decisions — 2026-08-13

## Compute
- **Primary now:** MacBook Pro M5, 48GB unified memory (MLX-friendly).
- **Secondary later:** Windows Ultra 9 + RTX 5080  (better for larger LoRA jobs).
- **Implication:** Phase 1 = RAG + small/quantized local models. Full 14B+ training waits for the Windows box unless we QLoRA carefully on Mac.

## Language
- **English only** for MVP (international).

## Knowledge sources
- Include Trustity product knowledge from day one.
- Ingested: `trustity.co` public pages + local marketing KB + local `trustity.dev` docs (`trustity-dev-central/content`).
- Live `trustity.dev` site is invite-only; local content tree is the source of truth for now.

## Weights openness (explained + default)
**Weights** = the trained model files people download.

| Option | Meaning |
|--------|---------|
| **Public on Hugging Face** | Anyone can download the model freely |
| **Gated** | People click “Request access”, you approve, then they download |

**Default for Trustity LLM v1:** **Gated on Hugging Face** + public chat demo on Labs.  
Why: niche security model + brand control while still being “open enough”. Can flip to fully public later.

## Base model (Mac-first revision)
1. **Serving on Mac now:** Qwen2.5-7B-Instruct or Llama-3.2-3B via **MLX** (quantized).
2. **LoRA target when Windows GPU online:** Qwen2.5-14B-Instruct.
3. Until fine-tune: **RAG over Trustity corpus** answers product questions accurately.
