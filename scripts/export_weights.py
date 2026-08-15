#!/usr/bin/env python3
"""Fuse Mac LoRA adapters into a portable checkpoint (optional Hugging Face upload).

The Mac trains. It does not serve the public site. After fuse you host the
weights on Hugging Face, Together, a small VPS, etc. Labs calls that API.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "mlx-community/Qwen2.5-3B-Instruct-4bit"
DEFAULT_ADAPTER = ROOT / "adapters" / "trustity-mlx"
DEFAULT_OUT = ROOT / "fused" / "trustity-qwen3b"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export fused Trustity LLM weights")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--adapter-path", default=str(DEFAULT_ADAPTER))
    parser.add_argument("--save-path", default=str(DEFAULT_OUT))
    parser.add_argument(
        "--upload-repo",
        default="",
        help="Hugging Face repo, e.g. Trustity/trustity-llm-qwen3b-lora",
    )
    args = parser.parse_args()

    adapter = Path(args.adapter_path)
    if not adapter.exists():
        sys.exit(f"No adapter at {adapter}. Train first: python3 scripts/train_lora_mlx.py")

    cmd = [
        sys.executable,
        "-m",
        "mlx_lm",
        "fuse",
        "--model",
        args.model,
        "--adapter-path",
        str(adapter),
        "--save-path",
        args.save_path,
    ]
    if args.upload_repo:
        cmd.extend(["--upload-repo", args.upload_repo])
    print(" ".join(cmd))
    subprocess.check_call(cmd)
    print(
        f"\nFused model at {args.save_path}\n"
        "Next: host it (HF endpoint, Together, or a small always-on VPS).\n"
        "Then set TRUSTITY_LLM_API_URL + TRUSTITY_LLM_API_KEY + TRUSTITY_LLM_MODEL on Vercel.\n"
        "See docs/MAC.md and serving/README.md."
    )


if __name__ == "__main__":
    main()
