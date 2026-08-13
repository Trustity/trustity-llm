# What are “weights”? (simple)

Think of an LLM like two parts:

1. **The brain’s knowledge files** → called **weights** (big files, GBs).
2. **The app that runs them** → chat UI / API (Labs, Hugging Face Space, etc.).

When we fine-tune Trustity LLM, we produce new weight files specialized for security + Trustity.

### Public weights
Upload to Hugging Face with no gate → anyone downloads and runs locally.

### Gated weights
Upload to Hugging Face with “Access request” → you approve users (email/org) → then they download.

### What we’re doing
- **Chat on Labs:** public (with rate limits).
- **Downloadable model files:** **gated** at first (our default), so we keep quality/brand control.

You don’t need to decide tooling today — this only affects the Hugging Face release button later.
