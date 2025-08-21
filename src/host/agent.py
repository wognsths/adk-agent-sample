from google.adk.agents import LlmAgent, SequentialAgent
import os, sys
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agents.company_search.agent import company_search_agent
from agents.financial_modeling.agent import financial_research_agent
from agents.fomc_research.agent import root_agent as fomc_research_agent

from .prompt import SYSTEM_INSTRUCTION
from .pdf_report_tool import create_markdown_report_tool

def set_api_key_for_agent(agent_name, key_number):
    api_key = os.getenv(f"GOOGLE_API_KEY{key_number}")
    os.environ["GOOGLE_API_KEY"] = api_key
    print(f"[{agent_name}] Using API Key {key_number}: {api_key[:10]}...")

# Company Search Agent
set_api_key_for_agent("company_search", 1)
company_search_agent_configured = company_search_agent

# FOMC Research Agent
set_api_key_for_agent("fomc_research", 2)
fomc_research_agent_configured = fomc_research_agent

# Financial Research Agent
set_api_key_for_agent("financial_research_agent", 3)
financial_research_agent_configured = financial_research_agent

# Analyzer
set_api_key_for_agent("analyzer",4)

integrated_search_agent = SequentialAgent(
    sub_agents=[
        financial_research_agent_configured,
        company_search_agent_configured,
        fomc_research_agent_configured, 
    ],
    name="parallel_investment_research_agent",
    description="Runs multiple research agents in parallel to gather information",
)

analyzer_agent = LlmAgent(
    model="gemini-2.5-pro",
    name="investment_research_synthesizer",
    description="Analyze the data from investment research and get final judgement on whether to invest or not.",
    instruction=SYSTEM_INSTRUCTION,
    tools=[create_markdown_report_tool]
)

investment_research_pipeline = SequentialAgent(
    name="investment_research_pipeline", 
    sub_agents=[integrated_search_agent, analyzer_agent]
)

root_agent = investment_research_pipeline