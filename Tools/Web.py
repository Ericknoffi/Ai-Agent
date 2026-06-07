# tools/fetch_mcp.py

from langchain_mcp_adapters.client import MultiServerMCPClient


async def get_fetch_tools():

    client = MultiServerMCPClient(
        {
            "fetch": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-fetch"
                ],
                "transport": "stdio"
            }
        }
    )

    return await client.get_tools()