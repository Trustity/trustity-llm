"""Shared BM25 retrieval: FAQ cards + corpus, with product alias expansion."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / "data" / "processed" / "corpus_chunks_v0.jsonl"
FAQ = ROOT / "data" / "seed" / "faq_v1.json"

TOKEN = re.compile(r"[a-z0-9_]+", re.I)
STOP = {
    "the",
    "and",
    "for",
    "that",
    "with",
    "this",
    "from",
    "what",
    "how",
    "why",
    "can",
    "does",
    "into",
    "your",
    "you",
    "are",
    "is",
    "a",
    "an",
    "of",
    "to",
    "in",
    "on",
    "or",
}

PRODUCT_ALIASES = {
    "visionx": ["visionx", "camera", "phone", "visual", "screen", "imaging", "lens", "lock"],
    "genguard": ["genguard", "genai", "chatgpt", "browser", "paste", "shadow", "llm", "dlp"],
    "hostguard": ["hostguard", "bruteforce", "brute", "rdp", "logon", "firewall", "ips"],
    "pam": ["pam", "vault", "rotation", "administrator", "credential", "password"],
    "axiom": ["axiom", "dns", "smb", "edge", "dga", "iot", "byod"],
    "secsend": ["secsend", "otp", "sms", "document", "delivery", "package"],
    "tao": ["tao", "agent", "portal", "heartbeat", "enrollment", "license"],
}

FAQ_BOOST = 1.85
MIN_SCORE = 3.2


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN.findall(text) if len(t) > 1]


def expand_query(question: str) -> list[str]:
    raw = question.lower()
    base = [t for t in tokenize(raw) if t not in STOP]
    out = set(base)
    blob = " " + " ".join(base) + " "
    for aliases in PRODUCT_ALIASES.values():
        if any(a in blob or a in raw for a in aliases):
            out.update(aliases)
    return list(out)[:28]


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


def faq_as_chunks() -> list[dict]:
    cards = json.loads(FAQ.read_text())
    out = []
    for card in cards:
        out.append(
            {
                "id": card["id"],
                "source_id": f"faq-{card['id']}",
                "title": card["title"],
                "origin": card["origin"],
                "text": card["answer"],
            }
        )
    return out


@lru_cache(maxsize=1)
def load_index() -> tuple[list[dict], BM25]:
    rows: list[dict] = faq_as_chunks()
    with CHUNKS.open() as f:
        for line in f:
            rows.append(json.loads(line))
    docs = []
    for c in rows:
        title = tokenize(c.get("title", ""))
        docs.append(title + title + title + tokenize(c.get("text", "")))
    return rows, BM25(docs)


def retrieve(question: str, k: int = 5) -> tuple[list[dict], bool, float]:
    chunks, bm25 = load_index()
    q = expand_query(question)
    ranked = []
    for i, chunk in enumerate(chunks):
        score = bm25.score(q, i)
        if str(chunk.get("source_id", "")).startswith("faq-"):
            score += FAQ_BOOST
        ranked.append((score, chunk))
    ranked.sort(key=lambda x: x[0], reverse=True)
    top = ranked[:k]
    hits = [{**c, "score": s} for s, c in top]
    top_score = hits[0]["score"] if hits else 0.0
    return hits, top_score < MIN_SCORE, top_score


SYSTEM = (
    "You are Trustity LLM, a defensive security specialist from Trustity Labs. "
    "Answer in English. Use ONLY the CONTEXT for Trustity product claims and cite [n]. "
    "If context is weak, say what is missing. Stay on security / Trustity. "
    "Refuse malware and unauthorized-attack help."
)


def build_prompt(question: str, contexts: list[dict]) -> str:
    blocks = []
    for i, c in enumerate(contexts, 1):
        blocks.append(
            f"[{i}] title={c.get('title')} origin={c.get('origin')}\n{c.get('text', '')[:1400]}"
        )
    ctx = "\n\n".join(blocks)
    return (
        f"{SYSTEM}\n\nCONTEXT:\n{ctx}\n\nQUESTION: {question}\n\n"
        "Write a concise, accurate answer. Cite context numbers like [1]."
    )
