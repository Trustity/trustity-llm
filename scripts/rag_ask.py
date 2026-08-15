#!/usr/bin/env python3
"""Trustity LLM RAG preview (BM25 + FAQ cards)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from retrieve import build_prompt, retrieve


def main() -> None:
    parser = argparse.ArgumentParser(description="Trustity LLM RAG preview (BM25)")
    parser.add_argument("question", nargs="?", help="Security / Trustity question")
    parser.add_argument("-k", type=int, default=4, help="Top chunks")
    parser.add_argument("--prompt-only", action="store_true")
    args = parser.parse_args()

    question = args.question or input("Question: ").strip()
    hits, weak, _ = retrieve(question, k=args.k)
    prompt = build_prompt(question, hits)
    if args.prompt_only:
        print(prompt)
        return

    print("=== Retrieved ===")
    for h in hits:
        print(f"- {h['score']:.3f} | {h.get('title')} | {h.get('origin')}")
    if weak:
        print("\n(weak retrieval — prefer 'I don't know' over guessing)\n")
    print("\n=== Grounded prompt ===\n")
    print(prompt)
    print("\n=== Extractive preview ===\n")
    print(hits[0].get("text", "")[:800])


if __name__ == "__main__":
    main()
