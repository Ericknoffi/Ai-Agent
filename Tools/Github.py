from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

async def get_github_tools():

    client = MultiServerMCPClient(
        {
            "github": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-github",
                ],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN":
                        GITHUB_TOKEN
                },
                "transport": "stdio",
            }
        }
    )

    return await client.get_tools()