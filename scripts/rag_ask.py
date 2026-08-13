#!/usr/bin/env python3
"""Minimal BM25 RAG over Trustity corpus — Mac-friendly, no GPU."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / "data" / "processed" / "corpus_chunks_v0.jsonl"

TOKEN = re.compile(r"[a-z0-9_]+", re.I)


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN.findall(text) if len(t) > 1]


class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.docs = docs
        self.k1 = k1
        self.b = b
        self.N = len(docs)
        self.avgdl = sum(len(d) for d in docs) / max(self.N, 1)
        self.df: Counter[str] = Counter()
        for d in docs:
            for t in set(d):
                self.df[t] += 1

    def idf(self, term: str) -> float:
        n = self.df.get(term, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def score(self, query: list[str], idx: int) -> float:
        doc = self.docs[idx]
        freqs = Counter(doc)
        dl = len(doc) or 1
        s = 0.0
        for t in query:
            if t not in freqs:
                continue
            tf = freqs[t]
            denom = tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            s += self.idf(t) * (tf * (self.k1 + 1)) / denom
        return s


def load_chunks() -> list[dict]:
    rows = []
    with CHUNKS.open() as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


SYSTEM = """You are Trustity LLM (preview, retrieval mode).
Answer using ONLY the provided Trustity context when possible.
If the context is insufficient, say what is missing.
Stay on security / Trustity topics. English only.
Refuse malware / unauthorized-attack requests.
"""


def build_prompt(question: str, contexts: list[dict]) -> str:
    blocks = []
    for i, c in enumerate(contexts, 1):
        blocks.append(
            f"[{i}] title={c.get('title')} origin={c.get('origin')}\n{c['text']}"
        )
    ctx = "\n\n".join(blocks)
    return (
        f"{SYSTEM}\n\n"
        f"CONTEXT:\n{ctx}\n\n"
        f"QUESTION: {question}\n\n"
        f"Write a concise, accurate answer. Cite context numbers like [1] when used."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Trustity LLM RAG preview (BM25)")
    parser.add_argument("question", nargs="?", help="Security / Trustity question")
    parser.add_argument("-k", type=int, default=4, help="Top chunks")
    parser.add_argument("--prompt-only", action="store_true", help="Print grounded prompt")
    args = parser.parse_args()

    question = args.question or input("Question: ").strip()
    chunks = load_chunks()
    docs = [tokenize(c["text"]) for c in chunks]
    bm25 = BM25(docs)
    q = tokenize(question)
    ranked = sorted(
        ((bm25.score(q, i), i) for i in range(len(chunks))),
        reverse=True,
    )[: args.k]
    contexts = [chunks[i] for score, i in ranked if score > 0]
    if not contexts:
        contexts = [chunks[i] for _, i in ranked]

    print("=== Retrieved ===")
    for score, i in ranked:
        c = chunks[i]
        print(f"- {score:.3f} | {c['title']} | {c['origin']}")

    prompt = build_prompt(question, contexts)
    print("\n=== Grounded prompt (paste into any LLM / later local MLX) ===\n")
    print(prompt)

    # Heuristic extractive answer for offline preview
    print("\n=== Extractive preview (no generative model yet) ===\n")
    print(contexts[0]["text"][:700])


if __name__ == "__main__":
    main()
