import sys
from langchain_mcp_adapters.client import MultiServerMCPClient


def create_fetch_client() -> MultiServerMCPClient:
    return MultiServerMCPClient(
        {
            "fetch": {
                "command": sys.executable,   # always correct venv Python, cross-platform
                "args": ["-m", "mcp_server_fetch"],
                "env": {"PYTHONIOENCODING": "utf-8"},
                "transport": "stdio",
            }
        }
    )
