from langchain_mcp_adapters.client import MultiServerMCPClient


async def get_filesystem_tools():

    client = MultiServerMCPClient(
        {
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    "./workspace",
                ],
                "transport": "stdio",
            }
        }
    )

    return await client.get_tools()