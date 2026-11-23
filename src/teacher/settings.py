"""Models, limits and environment, in one place."""

import os
from pathlib import Path

PROMPTS = Path(__file__).parent / "prompts"

SCRIPT_MODEL = "Qwen/Qwen3-14B-AWQ"
VOICE_MODEL = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
VOICE_CLONE_MODEL = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"  # imitates a reference clip (`teacher speak --clone`)
VOICE = "ryan"
LANGUAGE = "English"

CONTEXT = 16384  # script model window; the largest prompt is about 13k tokens
WORDS_PER_MINUTE = 150
SAMPLE_RATE = 24000
PAUSE_SECONDS = 0.6  # silence between paragraphs

PARALLEL = 16  # threads per parallel() call; each model's `parallel` profile setting caps its calls in flight

JUDGE_MODEL = "claude-sonnet-5-5"  # `teacher eval`'s judge: fixed, so scores stay comparable as the writer changes
CLAUDE_KEY = (
    "CLAUDE_API_KEY"  # read from the environment, or from a line in the repo's .env
)

# Each served model family's settings, matched by the start of its name. `writing` and `thinking` are the model
# settings of agents that write and of agents that plan or check; `server` is the extra `vllm serve` flags;
# `parallel` caps its calls in flight across all threads (vLLM batches them; the API takes more).
PROFILES = {
    # Qwen3's recommended sampling for each mode. Reply caps keep prompt + reply inside CONTEXT: a thinking call
    # can otherwise think until the window is full and return no answer. The KV cache is a fixed 3.5 GiB, about
    # 23k tokens of Qwen3-14B, next to 9.4 GiB of weights on a 16 GB card (4.5 GiB runs out of memory); vLLM's
    # own estimate collapses on a fresh compile.
    # JSON output allows no free whitespace: with it, the detailer's answer could turn into thousands of blank lines
    # until the token cap, then be retried. vLLM allows that option only with the backend named.
    "Qwen/Qwen3-": {
        "parallel": 6,
        "server": [
            *"--kv-cache-memory-bytes 3758096384 --max-num-seqs 8 --max-num-batched-tokens 2048".split(),
            *["--max-model-len", str(CONTEXT), "--reasoning-parser", "qwen3"],
            *[
                "--structured-outputs-config",
                '{"backend": "xgrammar", "disable_any_whitespace": true}',
            ],
        ],
        "writing": {
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.8,
            "extra_body": {
                "top_k": 20,
                "chat_template_kwargs": {"enable_thinking": False},
            },
        },
        "thinking": {
            "max_tokens": 6144,
            "temperature": 0.6,
            "top_p": 0.95,
            "extra_body": {
                "top_k": 20,
                "chat_template_kwargs": {"enable_thinking": True},
            },
        },
    },
    # Claude on the Anthropic API: thinking is always adaptive and effort sets its depth; no sampling settings.
    # A refused request is re-run on a fallback model in the same call (server-side fallback).
    "claude-": {
        "parallel": 16,
        "server": None,
        "writing": {
            "max_tokens": 16000,
            "anthropic_effort": "low",
            "anthropic_betas": ["server-side-fallback-2026-07-01"],
            "extra_body": {"fallbacks": "default"},
        },
        "thinking": {
            "max_tokens": 16000,
            "anthropic_effort": "high",
            "anthropic_betas": ["server-side-fallback-2026-07-01"],
            "extra_body": {"fallbacks": "default"},
        },
    },
}


def profile(model: str) -> dict:
    """The settings of the profile whose prefix `model` starts with."""
    for prefix, settings in PROFILES.items():
        if model.startswith(prefix):
            return settings
    raise ValueError(
        f"No profile in settings.PROFILES for {model!r}; add one for its family."
    )


for _name, _value in {
    "MINERU_TELEMETRY_DISABLED": "1",
    "VLLM_USE_FLASHINFER_SAMPLER": "0",  # FlashInfer JITs with the system nvcc; SM120 needs CUDA >= 12.9
    "MINERU_PROCESSING_WINDOW_SIZE": "8",  # PDF pages in RAM at once
    "TORCHINDUCTOR_COMPILE_THREADS": "1",
    # The CUDA driver's cache of kernels it compiled for this GPU. Every model here needs about 1.4 GB of them; at
    # the default 1 GiB, entries are evicted and recompiled, and a vLLM start can stall a minute in graph capture.
    "CUDA_CACHE_MAXSIZE": str(4 * 2**30),
}.items():
    os.environ.setdefault(_name, _value)
