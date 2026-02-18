run:
    uv run uvicorn app.main:app --reload

mcp:
    uv run python mcp_server.py

lint:
    uv tool run ruff check --fix
    uv tool run ruff format