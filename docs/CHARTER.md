# Trustity LLM — Product Charter

## One-liner

A **public security specialist LLM** from Trustity Labs: accurate niche answers for defensive / educational security questions, without depending on general-purpose chat services.

## Who it’s for

- Security practitioners and students asking practical questions
- People evaluating Trustity’s security philosophy / domain
- Eventually: light product-aware Q&A about Trustity capabilities (when docs are approved for public grounding)

## Who it’s not for

- Unrestricted general assistant
- “Write malware / attack this target” workflows
- Authoritative replacement for a human IR / compliance review

## Success criteria (MVP)

1. On a fixed **security eval suite**, beats a same-size general base model on niche accuracy + fewer hallucinations.
2. Stays on-topic: declines non-security chat politely.
3. Publicly reachable from Trustity Labs (demo or waitlist → chat).
4. Reproducible training recipe (base model, data mix, hyperparameters, eval).

## Capability tiers

### Must-have (v1)
- Explain defensive controls (DLP, PAM, host IPS concepts, browser GenAI risk, secure delivery)
- Hardening checklists and threat-model reasoning at educational depth
- Clear uncertainty (“I don’t know”) instead of inventing vendors/CVEs

### Nice-to-have (v1.x)
- Trustity product-aware answers grounded in public docs only
- Hebrew + English
- Citations to retrieved sources

### Later
- Tool use (query portal APIs) — out of scope until weights + RAG are solid

## Safety policy (public)

**Allow:** defensive guidance, education, detection ideas, secure configuration, high-level attack *concepts* for defense.

**Refuse:** actionable assistance for unauthorized intrusion, malware production for harm, bypassing controls on systems you don’t own.

Aligns with Trustity Labs experimental disclaimer.

## Positioning vs general LLMs

| General LLM | Trustity LLM |
|-------------|--------------|
| Broad world knowledge | Narrow, security-dense |
| Often invents product details | Grounded + eval-gated |
| One model for everything | Optimized for this niche |

## Openness

Default intent: **open recipe + public demo**.  
Weights: public on Hugging Face **or** gated Request Access — final call before Phase 2 release.
