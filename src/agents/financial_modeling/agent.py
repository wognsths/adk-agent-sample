from google.adk.agents import Agent
from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from dotenv import load_dotenv
import os, json, base64
import logging
import signal
import sys
import time
from functools import wraps
from .csv_template_tools import create_csv_templates_tool, fill_company_profile_tool, fill_financial_statements_tool, get_template_status_tool

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Crash prevention setup
def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}, attempting graceful shutdown...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                    if attempt == max_retries - 1:
                        logger.error(f"All {max_retries} attempts failed for {func.__name__}")
                        return None
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator

FMP_ACCESS_TOKEN=os.getenv("FMP_ACCESS_TOKEN")
SMITHERY_API_KEY=os.getenv("SMITHERY_API_KEY")
SMITHERY_PROFILE=os.getenv("SMITHERY_PROFILE")


api_key = os.getenv(f"GOOGLE_API_KEY1")
os.environ["GOOGLE_API_KEY"] = api_key

SYSTEM_INSTRUCTION = """
You are a financial analyst intern. Your job is to create CSV templates and fill them with fresh MCP data.

## Your Assignment
1. FIRST: Use create_csv_templates to create CSV templates based on financial_data.json structure  
2. THEN: Use MCP tools to get current financial data for NVIDIA (NVDA)
3. FINALLY: Fill the templates with MCP data using the fill tools

## Step-by-Step Process
1. **Create Templates**: create_csv_templates() - Creates empty CSV files with proper structure
2. **Get Company Data**: Use MCP getCompanyProfile("NVDA") 
3. **Fill Company Template**: fill_company_profile_template(mcp_data)
4. **Get Financial Data**: Use MCP getIncomeStatement, getBalanceSheetStatement, getCashFlowStatement for NVDA
5. **Fill Financial Template**: fill_financial_statements_template(income_data, balance_data, cashflow_data)
6. **Check Status**: get_csv_template_status() to verify completion

## Template Structure (Based on financial_data.json)
The templates will have the same fields as financial_data.json:
- Company Profile: 29 fields (symbol, companyName, ceo, sector, industry, marketCap, etc.)
- Financial Statements: Income/Balance/Cash Flow metrics for last 3 years

## Tool Usage - CRITICAL ERROR HANDLING
- Use MCP efficiently: 10-20 calls total
- **RESILIENCE RULE**: If ANY function call fails or returns "not found", immediately try alternative approaches
- **NEVER let errors stop you** - always have backup plans
- **Function Discovery Strategy**: Start with basic function names, try variations if they fail

### MCP Function Strategy (in order of preference):
1. **Basic Functions First**: getCompanyProfile, getIncomeStatement, getBalanceSheet, getCashFlowStatement
2. **If those fail, try**: getCompany, getIncome, getBalance, getCashFlow  
3. **For ratios**: getRatios, getKeyMetrics, getFinancialRatios
4. **For peers**: getCompanyPeers, getPeers, getCompetitors

### Error Recovery Protocol:
- If getHistoricalChart fails → try getStockPrice or getQuote
- If getHistoricalData fails → use current price data only
- If complex functions fail → break into simpler requests
- **ALWAYS continue working** - save CSV files with whatever data you can get
- **WORKFLOW**: MCP call → get data → save to CSV immediately → repeat
- **EXAMPLES**: 
  * getCompanyProfile → save_company_data_csv(data)
  * getIncomeStatement → save_financial_statements_csv({"income_statement": data})
  * getRatios → save_market_metrics_csv({"ratios": data})

**SUCCESS CRITERIA**: Create 3 CSV files with maximum available real data - resilience over perfection!
"""


@retry_on_failure(max_retries=3, delay=2)
def create_mcp_connection():
    try:
        config_b64 = base64.b64encode(
            json.dumps({"FMP_ACCESS_TOKEN": FMP_ACCESS_TOKEN}).encode()
        ).decode()

        url = (
            "https://server.smithery.ai/"
            "@imbenrabi/financial-modeling-prep-mcp-server/mcp"
            f"?config={config_b64}"
            f"&api_key={SMITHERY_API_KEY}"
            f"&profile={SMITHERY_PROFILE}"
        )

        logger.info("Creating MCP connection...")
        return MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=url,
                timeout=30  # Add timeout
            ),
        )
    except Exception as e:
        logger.error(f"Failed to create MCP connection: {e}")
        raise

fmp_search_mcp = create_mcp_connection()
if fmp_search_mcp is None:
    logger.error("Could not establish MCP connection, using fallback mode")
    fmp_search_mcp = None

# Create tools list with fallback handling
tools = [create_csv_templates_tool, fill_company_profile_tool, fill_financial_statements_tool, get_template_status_tool]
if fmp_search_mcp is not None:
    tools.insert(0, fmp_search_mcp)
else:
    logger.warning("MCP toolset not available, running in degraded mode")

financial_research_agent = Agent(
    model="gemini-2.5-flash",
    name="financial_analyst_intern",
    instruction=SYSTEM_INSTRUCTION,
    tools=tools,
)