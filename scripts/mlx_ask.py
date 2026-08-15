#!/usr/bin/env python3
"""Local Mac path: BM25 retrieve + MLX generate, optional LoRA adapter."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from retrieve import SYSTEM, build_prompt, retrieve  # noqa: E402

DEFAULT_MODEL = "mlx-community/Qwen2.5-3B-Instruct-4bit"
DEFAULT_ADAPTER = ROOT / "adapters" / "trustity-mlx"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--adapter",
        default=str(DEFAULT_ADAPTER) if DEFAULT_ADAPTER.exists() else "",
        help="LoRA adapter directory from train_lora_mlx.py",
    )
    parser.add_argument("-k", type=int, default=4)
    parser.add_argument("--max-tokens", type=int, default=450)
    args = parser.parse_args()

    hits, weak, top = retrieve(args.question, k=args.k)
    print("=== Retrieved ===")
    for h in hits:
        print(f"- {h['score']:.3f} | {h.get('title')} | {h.get('origin')}")
    if weak:
        print(
            "\nContext is weak; the model should say what is missing rather than invent product behavior.\n"
        )

    prompt = build_prompt(args.question, hits)

    try:
        from mlx_lm import generate, load
    except ImportError:
        print(prompt[:2000])
        print(
            "\nmlx-lm not installed.\n"
            "  python3 -m venv .venv && source .venv/bin/activate\n"
            "  pip install -r requirements-mlx.txt\n"
            "Then re-run this command."
        )
        return

    load_kwargs = {}
    if args.adapter:
        load_kwargs["adapter_path"] = args.adapter
        print(f"Loading {args.model} + adapter {args.adapter}")
    else:
        print(f"Loading {args.model} (base, no LoRA)")

    model, tokenizer = load(args.model, **load_kwargs)
    ctx_blocks = []
    for i, c in enumerate(hits, 1):
        ctx_blocks.append(
            f"[{i}] title={c.get('title')} origin={c.get('origin')}\n{c.get('text', '')[:1400]}"
        )
    user = (
        "CONTEXT:\n"
        + "\n\n".join(ctx_blocks)
        + f"\n\nQUESTION: {args.question}\n\n"
        "Answer concisely. Cite [n]. If context is weak, say so."
    )
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
    ]
    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template:
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
    else:
        text = build_prompt(args.question, hits)

    answer = generate(
        model,
        tokenizer,
        prompt=text,
        max_tokens=args.max_tokens,
        verbose=False,
    )
    print("\n=== Trustity LLM (MLX) ===\n")
    print(answer.strip())


if __name__ == "__main__":
    main()
