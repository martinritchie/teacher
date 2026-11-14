# Teacher 

Converts ML/AI papers into an audio only format, like a podcast.

🔥🔥 _This is an experimental repo, I am currently iterating on generating narratives over any engineering work._ 🔥🔥

I am a busy parent, this helps me keep on top of reading: doing the dishes, driving and that sort of thing. No replacement for reading but better than no reading.

## Usage

Install [Ollama](https://ollama.com), pull a model, and install espeak-ng for Kokoro:

```bash
ollama pull gemma3:12b
sudo apt install espeak-ng  # Ubuntu
uv sync
```

One command turns a PDF path, PDF URL, arXiv abs URL or blog post URL into `<out>/<name>.md` (the script) and `<out>/<name>.mp3`:

```bash
uv run teacher run https://arxiv.org/abs/2510.27688 --minutes 20
```

Options: `--model` (Ollama tag, default `gemma3:12b`), `--voice` (Kokoro voice, default `af_heart`), `--minutes` (default 25), `--chunk` (max source tokens per call, default 4000; lower it if the run stops with a cut prompt), `--out` (default `out`).

## Development Plan