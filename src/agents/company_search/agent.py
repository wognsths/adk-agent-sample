from google.adk.agents import Agent
from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from dotenv import load_dotenv
import os, json, base64
from datetime import datetime

load_dotenv()

SMITHERY_API_KEY=os.getenv("SMITHERY_API_KEY")
SMITHERY_PROFILE=os.getenv("SMITHERY_PROFILE")


SYSTEM_INSTRUCTION="""
You are an expert researcher of company, with using EXA search tool.

You should research the company client requested for, with comprehensive information of business, organizations and etc.
You should also search for the competitors for the company's business field.

You should search for recent information, unless the client requests with specific date.

After completing each search, please return as much information as possible without summarizing.
"""


config = {
    "debug": False
}
config_b64 = base64.b64encode(json.dumps(config).encode()).decode()
exa_server_url = f"https://server.smithery.ai/exa/mcp?config={config_b64}&api_key={SMITHERY_API_KEY}&profile={SMITHERY_PROFILE}"
exa_search_mcp = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=exa_server_url
    ),
)


company_search_agent = Agent(
    model="gemini-2.5-flash",
    name="company_search_agent",
    instruction=SYSTEM_INSTRUCTION,
    tools=[exa_search_mcp],
)