# Base model shortlist (Phase 0)

Decision pending compute confirmation. Order = current preference.

| Rank | Model | Why | Serving cost |
|------|-------|-----|--------------|
| 1 | Qwen2.5-14B-Instruct | Strong instruction following, good reasoning, open | Medium |
| 2 | Llama-3.1-8B-Instruct | Cheap to fine-tune & host; solid baseline | Low |
| 3 | Qwen2.5-32B-Instruct | Higher quality if GPU budget allows | High |
| 4 | Llama-3.1-70B-Instruct | Teacher model for synthetic data (not necessarily deployed) | High |

**Training approach:** LoRA/QLoRA SFT, not full fine-tune, until data volume justifies otherwise.

**Teacher (synthetic):** larger general model *only* to draft candidates; humans / eval filters keep niche quality.
