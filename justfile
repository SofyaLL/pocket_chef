run:
    uv run uvicorn app.main:app --reload

mcp:
    fastmcp run app/mcp.py:mcp

lint:
    uv tool run ruff check --fix
    uv tool run ruff format