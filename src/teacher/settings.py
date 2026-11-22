"""Models, limits and environment, in one place."""

import os
from pathlib import Path

PROMPTS = Path(__file__).parent / "prompts"

SCRIPT_MODEL = "Qwen/Qwen3-14B-AWQ"
VOICE_MODEL = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
VOICE = "ryan"
LANGUAGE = "English"

CONTEXT = 16384  # script model window; the largest prompt is about 13k tokens
WORDS_PER_MINUTE = 150
SAMPLE_RATE = 24000
PAUSE_SECONDS = 0.6  # silence between paragraphs

PARALLEL = 4  # model calls in flight at once; vLLM batches them (continuous batching)

# The KV cache is a fixed 3.5 GiB, about 23k tokens of Qwen3-14B: room for a few calls at once next to
# 9.4 GiB of weights on a 16 GB card (4.5 GiB runs out of memory). vLLM's own estimate collapses on a fresh compile.
SCRIPT_SERVER_ARGS = [
    *"--kv-cache-memory-bytes 3758096384 --max-num-seqs 8 --max-num-batched-tokens 2048".split(),
    *["--max-model-len", str(CONTEXT), "--reasoning-parser", "qwen3"],
]

# Qwen3's recommended sampling for each mode. Reply caps keep prompt + reply inside CONTEXT:
# a thinking call can otherwise think until the window is full and return no answer.
WRITING = {
    "max_tokens": 2048,
    "temperature": 0.7,
    "top_p": 0.8,
    "extra_body": {"top_k": 20, "chat_template_kwargs": {"enable_thinking": False}},
}
THINKING = {
    "max_tokens": 6144,
    "temperature": 0.6,
    "top_p": 0.95,
    "extra_body": {"top_k": 20, "chat_template_kwargs": {"enable_thinking": True}},
}

for _name, _value in {
    "MINERU_TELEMETRY_DISABLED": "1",
    "VLLM_USE_FLASHINFER_SAMPLER": "0",  # FlashInfer JITs with the system nvcc; SM120 needs CUDA >= 12.9
    "MINERU_PROCESSING_WINDOW_SIZE": "8",  # PDF pages in RAM at once
    "TORCHINDUCTOR_COMPILE_THREADS": "1",
}.items():
    os.environ.setdefault(_name, _value)
