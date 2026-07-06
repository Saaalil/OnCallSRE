import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class GitLabMCPClient:
    def __init__(self, gitlab_url="https://gitlab.com/api/v4/mcp"):
        self.gitlab_url = gitlab_url
        self._session = None
        self._exit_stack = None

    async def connect(self):
        """
        Connects to the GitLab MCP Server using mcp-remote proxy via npx.
        This automatically handles OAuth via browser popups on first run.
        """
        from contextlib import AsyncExitStack
        self._exit_stack = AsyncExitStack()
        
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "mcp-remote", self.gitlab_url],
            env=None
        )

        read, write = await self._exit_stack.enter_async_context(stdio_client(server_params))
        self._session = await self._exit_stack.enter_async_context(ClientSession(read, write))
        
        await self._session.initialize()
        print("[GitLabMCPClient] Connected to GitLab MCP Server!")

    async def get_tools(self):
        """Fetches available tools from the MCP server."""
        if not self._session:
            raise Exception("Client not connected")
        response = await self._session.list_tools()
        return response.tools

    async def call_tool(self, tool_name: str, arguments: dict):
        """Calls a specific tool on the MCP server."""
        if not self._session:
            raise Exception("Client not connected")
        print(f"[GitLabMCPClient] Calling tool '{tool_name}' with args {arguments}...")
        result = await self._session.call_tool(tool_name, arguments)
        return result

    async def disconnect(self):
        """Closes the connection to the MCP server."""
        if self._exit_stack:
            await self._exit_stack.aclose()
            print("[GitLabMCPClient] Disconnected.")

# Synchronous wrapper for agents
def call_gitlab_tool_sync(tool_name: str, arguments: dict):
    """
    Synchronous helper to run the MCP tool. 
    Currently mocked out completely for the hackathon demo to prevent Node/AnyIO background errors.
    """
    print(f"[GitLabMCPClient] Mocking call to '{tool_name}' for demo purposes...")
    
    if tool_name == "create_merge_request":
        return "https://gitlab.example.com/project/-/merge_requests/12345"
        
    # Raise exception to force agents (like ObservabilityAgent) to use their rich fallback data
    raise Exception("Simulated MCP tool absence")
