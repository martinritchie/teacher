# Teacher 

Converts ML/AI papers into an audio only format, like a podcast.

🔥🔥 _This is an experimental repo, I am currently iterating on generating narratives over any engineering work._ 🔥🔥

I am a busy parent, this helps me keep on top of reading: doing the dishes, driving and that sort of thing. No replacement for reading but better than no reading.

## Getting Started 

### Env

Set your api keys, see `./env.example`.

### Installation

```bash
git clone ...
uv sync --all-extras
teacher --help
```

## Data Flow 

1. A anthropic [haiku](https://assets.anthropic.com/m/99128ddd009bdcb/Claude-Haiku-4-5-System-Card.pdf) based agent parses a pdf into markdown.

```bash
teacher reader --help
```

2. A direct LLM call prompted with few shot examples as well as a markdown paper section from `reader`.

```bash
teacher writer --help
```

3. A TTS service is then used to produce the audio:

```bash
teacher speaker --help
```

4. Development pipeline for quick iteration:

```bash
teacher dev --help
```
## Development Plan