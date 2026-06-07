from langchain_mcp_adapters.client import MultiServerMCPClient


async def get_context7_tools():

    client = MultiServerMCPClient(
        {
            "context7": {
                "command": "npx",
                "args": [
                    "-y",
                    "@upstash/context7-mcp"
                ],
                "transport": "stdio"
            }
        }
    )

    return await client.get_tools()