# Data policy

## Principles

1. **Public-first for v1** — prefer licenses that allow training + redistribution.
2. **No customer secrets** — never train on tenant data, raw logs with PII, or private keys.
3. **Trustity product docs** — only if explicitly approved for public grounding / training.
4. **Synthetic data OK** — must be filtered for accuracy and safety.
5. **Provenance** — every processed shard records source + license + date.

## Allowed source classes (planned)

| Class | Examples | Notes |
|-------|----------|-------|
| Public security primers | OWASP, NIST high-level, CISA advisories (check license) | Prefer summaries we rewrite |
| Curated Q&A we author | Trustity Labs seed set | Highest trust |
| Synthetic SFT | Generated then human/model-filtered | Large volume |
| Approved Trustity public docs | marketing/KB pages marked public | Product-aware mode |

## Denied

- Private portal tickets / customer configs
- Copyrighted books pasted wholesale
- Exploit DB dumps used to teach end-to-end attack reproduction

## Formats

- Training: JSONL `{ "messages": [{"role","content"}, ...] }`
- Eval: JSONL `{ "id", "question", "reference", "tags", "must_refuse?" }`
