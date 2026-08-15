"""OpenAI-compatible chat server for Railway (CPU GGUF).

Labs on Vercel calls POST /v1/chat/completions. This process stays up;
the Mac is not in the path.
"""

from __future__ import annotations

import os
import threading
import time
from contextlib import asynccontextmanager
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
N_THREADS = int(os.environ.get("N_THREADS", "1"))

_llm = None
_ready = False
_infer_lock = threading.Lock()


def get_llm():
    global _llm
    if _llm is not None:
        return _llm
    from huggingface_hub import hf_hub_download
    from llama_cpp import Llama

    print(f"Downloading {MODEL_REPO}/{MODEL_FILE} …", flush=True)
    path = hf_hub_download(repo_id=MODEL_REPO, filename=MODEL_FILE)
    print(f"Loading GGUF from {path}", flush=True)
    _llm = Llama(
        model_path=path,
        n_ctx=N_CTX,
        n_threads=N_THREADS,
        n_threads_batch=N_THREADS,
        n_batch=int(os.environ.get("N_BATCH", "256")),
        n_gpu_layers=0,
        verbose=False,
    )
    print("Model ready", flush=True)
    return _llm


@asynccontextmanager
async def lifespan(_: FastAPI):
    global _ready
    get_llm()
    _ready = True
    yield


app = FastAPI(title="Trustity LLM", version="0.1.0", lifespan=lifespan)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str | None = None
    messages: list[ChatMessage]
    temperature: float = 0.15
    max_tokens: int = Field(default=256, le=512)


def require_key(authorization: str | None) -> None:
    if not API_KEY:
        return
    token = (authorization or "").removeprefix("Bearer ").strip()
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")


@app.get("/health")
def health() -> dict[str, str]:
    if not _ready:
        raise HTTPException(status_code=503, detail="model loading")
    return {"status": "ok", "model": MODEL_FILE}


@app.post("/v1/chat/completions")
def chat(
    body: ChatRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    require_key(authorization)
    llm = get_llm()
    prompt_parts: list[str] = []
    for m in body.messages:
        prompt_parts.append(f"<|im_start|>{m.role}\n{m.content}<|im_end|>")
    prompt_parts.append("<|im_start|>assistant\n")
    prompt = "\n".join(prompt_parts)
    print(f"infer start tokens={min(body.max_tokens, 256)} prompt_chars={len(prompt)}", flush=True)
    with _infer_lock:
        t0 = time.time()
        out = llm.create_completion(
            prompt=prompt,
            temperature=body.temperature,
            max_tokens=min(body.max_tokens, 256),
            stop=["<|im_end|>", "<|endoftext|>"],
        )
        print(f"infer done in {time.time() - t0:.2f}s", flush=True)
    text = (out.get("choices") or [{}])[0].get("text", "")
    created = int(time.time())
    return {
        "id": out.get("id", "trustity-llm"),
        "object": "chat.completion",
        "created": created,
        "model": body.model or MODEL_FILE,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": (out.get("choices") or [{}])[0].get("finish_reason", "stop"),
            }
        ],
        "usage": out.get("usage", {}),
    }
