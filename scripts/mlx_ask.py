#!/usr/bin/env python3
"""Local Mac generative path: BM25 retrieve + MLX model (optional).

Install (Apple Silicon):
  pip install mlx-lm

Example:
  python scripts/mlx_ask.py "What does VisionX detect?" --model mlx-community/Qwen2.5-7B-Instruct-4bit
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def retrieve_prompt(question: str) -> str:
    rag = ROOT / "scripts" / "rag_ask.py"
    return subprocess.check_output(
        [sys.executable, str(rag), question, "--prompt-only", "-k", "4"],
        text=True,
    ).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument(
        "--model",
        default="mlx-community/Qwen2.5-3B-Instruct-4bit",
        help="MLX community model id",
    )
    args = parser.parse_args()

    prompt = retrieve_prompt(args.question)
    print("=== Prompt ready (truncated) ===\n")
    print(prompt[:1500], "...\n")

    try:
        from mlx_lm import load, generate  # type: ignore
    except ImportError:
        print(
            "mlx-lm not installed. Retrieval prompt is ready above.\n"
            "Install with: pip install mlx-lm\n"
            "Then re-run to generate on the M5 Mac.",
        )
        return

    print(f"Loading {args.model} …")
    model, tokenizer = load(args.model)
    answer = generate(model, tokenizer, prompt=prompt, max_tokens=500, verbose=False)
    print("\n=== Trustity LLM (MLX) ===\n")
    print(answer)


if __name__ == "__main__":
    main()
