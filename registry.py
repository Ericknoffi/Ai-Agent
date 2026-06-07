from Agent.Tools.Filesystem import get_filesystem_tools
from Agent.Tools.Github import get_github_tools
from Agent.Tools.Web import get_fetch_tools
from Agent.Tools.Documentation import get_context7_tools

RESEARCH_TOOLS = []
CODING_TOOLS = []


async def initialize_tools():

    global RESEARCH_TOOLS
    global CODING_TOOLS

    RESEARCH_TOOLS = [
        *await get_filesystem_tools(),
        *await get_github_tools(),
        *await get_fetch_tools(),
    ]

    CODING_TOOLS = [
        *await get_filesystem_tools(),
        *await get_github_tools(),
        *await get_context7_tools(),
    ]