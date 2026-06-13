from langchain_mcp_adapters.client import MultiServerMCPClient


def create_context7_client() -> MultiServerMCPClient:
    return MultiServerMCPClient(
        {
            "context7": {
                "command": "npx",
                "args": ["-y", "@upstash/context7-mcp"],
                "transport": "stdio",
            }
        }
    )
