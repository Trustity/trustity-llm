"""OpenAI-compatible chat server for Railway (CPU GGUF).

Labs on Vercel calls POST /v1/chat/completions. This process stays up;
the Mac is not in the path.
"""

from __future__ import annotations

import os
import time
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

MODEL_REPO = os.environ.get(
    "MODEL_REPO", "bartowski/Qwen2.5-3B-Instruct-GGUF"
)
MODEL_FILE = os.environ.get(
    "MODEL_FILE", "Qwen2.5-3B-Instruct-Q4_K_M.gguf"
)
API_KEY = os.environ.get("LLM_API_KEY", "").strip()
N_CTX = int(os.environ.get("N_CTX", "2048"))
N_THREADS = int(os.environ.get("N_THREADS", str(os.cpu_count() or 4)))

app = FastAPI(title="Trustity LLM", version="0.1.0")
_llm = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str | None = None
    messages: list[ChatMessage]
    temperature: float = 0.15
    max_tokens: int = Field(default=500, le=1024)


def require_key(authorization: str | None) -> None:
    if not API_KEY:
        return
    token = (authorization or "").removeprefix("Bearer ").strip()
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")


def get_llm():
    global _llm
    if _llm is not None:
        return _llm
    from huggingface_hub import hf_hub_download
    from llama_cpp import Llama

    path = hf_hub_download(repo_id=MODEL_REPO, filename=MODEL_FILE)
    _llm = Llama(
        model_path=path,
        n_ctx=N_CTX,
        n_threads=N_THREADS,
        n_gpu_layers=0,
        chat_format="qwen",
        verbose=False,
    )
    return _llm


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": MODEL_FILE}


@app.post("/v1/chat/completions")
def chat(
    body: ChatRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    require_key(authorization)
    llm = get_llm()
    messages = [{"role": m.role, "content": m.content} for m in body.messages]
    out = llm.create_chat_completion(
        messages=messages,
        temperature=body.temperature,
        max_tokens=body.max_tokens,
    )
    created = int(time.time())
    choice = out["choices"][0]
    return {
        "id": out.get("id", "trustity-llm"),
        "object": "chat.completion",
        "created": created,
        "model": body.model or MODEL_FILE,
        "choices": [
            {
                "index": 0,
                "message": choice.get("message", {}),
                "finish_reason": choice.get("finish_reason", "stop"),
            }
        ],
        "usage": out.get("usage", {}),
    }
