import os
from langchain_mcp_adapters.client import MultiServerMCPClient


def create_github_client() -> MultiServerMCPClient | None:
    # Read at call time so load_dotenv() in main.py always runs first
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return None

    return MultiServerMCPClient(
        {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": token},
                "transport": "stdio",
            }
        }
    )
