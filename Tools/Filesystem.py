import os
from langchain_mcp_adapters.client import MultiServerMCPClient


def create_filesystem_client(workspace_path: str) -> MultiServerMCPClient:
    os.makedirs(workspace_path, exist_ok=True)  # create if missing — server fails without it

    return MultiServerMCPClient(
        {
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    workspace_path,        # use absolute path — no cwd dependency
                ],
                "transport": "stdio",
            }
        }
    )
