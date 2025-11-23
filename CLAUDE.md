# CLAUDE.md

I am the only user of this library and my current development efforts are focused on prompts. When requests to write code, always implement the functionality in as few lines as possible. 

1. Use `uv` for running code and managing deps. 
2. After writing code run `uv run ruff format .` and `uv run ruff check --fix .`
3. Where it makes sense to, expose functionality with a typer based cli. Use the one file per command pattern and centralise the calls through [teacher](./src/teacher/cli.py)