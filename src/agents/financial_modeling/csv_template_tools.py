from google.adk.tools import FunctionTool
from typing import Dict, Any, List
import os
from .csv_template_handler import CSVTemplateHandler

# Global template handler instance
_template_handler = None

def get_template_handler():
    global _template_handler
    if _template_handler is None:
        database_dir = os.path.join(os.path.dirname(__file__), "database")
        _template_handler = CSVTemplateHandler(database_dir)
    return _template_handler

def create_csv_templates() -> str:
    """Create CSV templates based on financial_data.json structure.
    
    This creates empty CSV templates with the same structure as financial_data.json
    that can be filled with MCP data.
    
    Returns:
        str: Confirmation message about template creation
    """
    try:
        handler = get_template_handler()
        
        results = []
        results.append(handler.create_company_profile_template())
        results.append(handler.create_financial_statements_template())
        
        status = handler.get_template_status()
        
        return f"CSV Templates Created!\\n\\n" + "\\n".join(results) + f"\\n\\n{status}"
        
    except Exception as e:
        return f"Error creating CSV templates: {str(e)}"

def fill_company_profile_template(mcp_data: Dict[str, Any]) -> str:
    """Fill company profile template with MCP data.
    
    Args:
        mcp_data: Company profile data from MCP call
        
    Returns:
        str: Confirmation message
    """
    try:
        handler = get_template_handler()
        return handler.fill_company_profile_with_mcp_data(mcp_data)
    except Exception as e:
        return f"Error filling company profile template: {str(e)}"

def fill_financial_statements_template(income_data: List[Dict[str, Any]], 
                                     balance_data: List[Dict[str, Any]], 
                                     cashflow_data: List[Dict[str, Any]]) -> str:
    """Fill financial statements template with MCP data.
    
    Args:
        income_data: Income statement data from MCP call
        balance_data: Balance sheet data from MCP call  
        cashflow_data: Cash flow statement data from MCP call
        
    Returns:
        str: Confirmation message
    """
    try:
        handler = get_template_handler()
        return handler.fill_financial_statements_with_mcp_data(income_data, balance_data, cashflow_data)
    except Exception as e:
        return f"Error filling financial statements template: {str(e)}"

def get_csv_template_status() -> str:
    """Get status of CSV templates.
    
    Returns:
        str: Status of CSV templates
    """
    try:
        handler = get_template_handler()
        return handler.get_template_status()
    except Exception as e:
        return f"Error getting template status: {str(e)}"

# Create FunctionTool instances
create_csv_templates_tool = FunctionTool(create_csv_templates)
fill_company_profile_tool = FunctionTool(fill_company_profile_template)
fill_financial_statements_tool = FunctionTool(fill_financial_statements_template)
get_template_status_tool = FunctionTool(get_csv_template_status)