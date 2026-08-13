# Trustity LLM

Public, security-specialized language model from **[Trustity Labs](https://labs.trustity.co)**.

> Not a general chatbot. Built to answer **security** questions with higher niche accuracy than ChatGPT / Gemini-style general models.

**Status:** foundation · Phase 0  
**Org:** [Trustity](https://trustity.co) · Labs research surface

---

## Mission

Ship an open (or gated-open) assistant that people can ask about:

- Endpoint / browser DLP concepts
- Credential & PAM hygiene
- Host / network defensive controls
- Secure delivery & edge patterns
- Practical hardening and incident reasoning

…without relying on a general-purpose LLM that invents product details or drifts off-niche.

---

## Product decisions (locked for MVP)

| Decision | Choice |
|----------|--------|
| Audience | Public |
| Scope | Security Q&A (defensive + educational) |
| Non-goals (MVP) | General chat, coding agent, unrestricted offensive tooling |
| Delivery | Chat surface on Trustity Labs + optional Hugging Face |
| Training strategy | Strong open base → curated data → LoRA/SFT → eval → iterate |
| Safety | Refuse clear crime-assist / malware-for-harm; allow defensive education |

Full charter: [`docs/CHARTER.md`](docs/CHARTER.md)  
Roadmap: [`docs/ROADMAP.md`](docs/ROADMAP.md)

---

## Phases

1. **Phase 0 — Foundation** *(now)* · repo, charter, seed eval, data plan  
2. **Phase 1 — RAG MVP** · curated security corpus + retrieval demo on Labs  
3. **Phase 2 — Specialist weights** · LoRA/SFT on chosen base + public eval scores  
4. **Phase 3 — Public chat** · Labs UI, rate limits, Request Access / HF

---

## Repo layout

```
apps/chat/          # Labs-facing chat UI (later)
configs/            # model + training configs
data/raw/           # ingested sources (gitignored if sensitive)
data/processed/     # train/eval JSONL
data/seed/          # small public seed sets
docs/               # charter, roadmap, data policy
eval/               # suites + scored results
serving/            # inference / API
training/           # fine-tune scripts
scripts/            # ETL helpers
```

---

## Quick links

- Labs portal: https://labs.trustity.co  
- Brand: https://trustity.co  

## Disclaimer

Experimental engineering. Not for production security decisions without human review.
