#!/usr/bin/env python3
"""LoRA fine-tune Trustity LLM on Apple Silicon via mlx-lm."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "sft_v0"
ADAPTERS = ROOT / "adapters" / "trustity-mlx"

DEFAULT_MODEL = "mlx-community/Qwen2.5-3B-Instruct-4bit"


def main() -> None:
    parser = argparse.ArgumentParser(description="Train Trustity LoRA with MLX")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--iters", type=int, default=200)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--lora-layers", type=int, default=8)
    parser.add_argument("--adapter-path", default=str(ADAPTERS))
    args = parser.parse_args()

    if not (DATA / "train.jsonl").exists():
        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "build_sft.py")])

    cmd = [
        sys.executable,
        "-m",
        "mlx_lm",
        "lora",
        "--model",
        args.model,
        "--data",
        str(DATA),
        "--adapter-path",
        args.adapter_path,
        "--fine-tune-type",
        "lora",
        "--train",
        "--mask-prompt",
        "--iters",
        str(args.iters),
        "--batch-size",
        str(args.batch_size),
        "--num-layers",
        str(args.lora_layers),
        "--learning-rate",
        "1e-4",
        "--max-seq-length",
        "1536",
        "--steps-per-report",
        "10",
        "--steps-per-eval",
        "50",
        "--save-every",
        "100",
    ]
    print(" ".join(cmd))
    subprocess.check_call(cmd)


if __name__ == "__main__":
    main()
