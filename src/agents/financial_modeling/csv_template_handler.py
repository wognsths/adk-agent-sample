import csv
import os
from datetime import datetime
from typing import Dict, Any

class CSVTemplateHandler:
    """Creates CSV templates based on financial_data.json structure and fills them with MCP data."""
    
    def __init__(self, database_dir: str = "database"):
        self.database_dir = database_dir
        self._ensure_database_dir()
    
    def _ensure_database_dir(self):
        """Create database directory if it doesn't exist."""
        if not os.path.exists(self.database_dir):
            os.makedirs(self.database_dir)
    
    def create_company_profile_template(self) -> str:
        """Create company profile CSV template based on financial_data.json structure."""
        csv_path = os.path.join(self.database_dir, "nvidia_company_profile.csv")
        
        headers = ['Field', 'Value', 'Timestamp']
        
        # Template rows based on financial_data.json structure
        template_rows = [
            ['Symbol', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Company Name', '[MCP_DATA]', '[TIMESTAMP]'],
            ['CEO', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Sector', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Industry', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Exchange', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Exchange Full Name', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Website', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Full Time Employees', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Market Cap', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Current Price', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Currency', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Volume', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Average Volume', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Price Range', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Beta', '[MCP_DATA]', '[TIMESTAMP]'],
            ['IPO Date', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Last Dividend', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Change', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Change Percentage', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Country', '[MCP_DATA]', '[TIMESTAMP]'],
            ['State', '[MCP_DATA]', '[TIMESTAMP]'],
            ['City', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Address', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Phone', '[MCP_DATA]', '[TIMESTAMP]'],
            ['CUSIP', '[MCP_DATA]', '[TIMESTAMP]'],
            ['ISIN', '[MCP_DATA]', '[TIMESTAMP]'],
            ['CIK', '[MCP_DATA]', '[TIMESTAMP]'],
            ['Description', '[MCP_DATA]', '[TIMESTAMP]']
        ]
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(template_rows)
        
        return f"Company profile template created at {csv_path} with {len(template_rows)} fields"
    
    def create_financial_statements_template(self) -> str:
        """Create financial statements CSV template based on financial_data.json structure."""
        csv_path = os.path.join(self.database_dir, "nvidia_financial_statements.csv")
        
        headers = ['Statement_Type', 'Metric', 'Value', 'Period', 'Fiscal_Year', 'Date', 'Timestamp']
        
        # Template rows for last 3 years based on financial_data.json structure
        template_rows = []
        years = ['2025', '2024', '2023']
        
        for year in years:
            # Income Statement metrics
            template_rows.extend([
                ['Income Statement', 'Revenue', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Income Statement', 'Gross Profit', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Income Statement', 'Operating Income', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Income Statement', 'Net Income', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Income Statement', 'EPS', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Income Statement', 'EPS Diluted', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Income Statement', 'EBITDA', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Income Statement', 'R&D Expenses', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]']
            ])
            
            # Balance Sheet metrics
            template_rows.extend([
                ['Balance Sheet', 'Total Assets', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Balance Sheet', 'Total Liabilities', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Balance Sheet', 'Total Equity', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Balance Sheet', 'Cash and Cash Equivalents', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Balance Sheet', 'Total Debt', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Balance Sheet', 'Inventory', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Balance Sheet', 'Accounts Receivables', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]']
            ])
            
            # Cash Flow metrics
            template_rows.extend([
                ['Cash Flow', 'Operating Cash Flow', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Cash Flow', 'Free Cash Flow', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Cash Flow', 'Capital Expenditure', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Cash Flow', 'Net Income', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]'],
                ['Cash Flow', 'Dividends Paid', '[MCP_DATA]', 'FY', year, '[MCP_DATE]', '[TIMESTAMP]']
            ])
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(template_rows)
        
        return f"Financial statements template created at {csv_path} with {len(template_rows)} metrics"
    
    def fill_company_profile_with_mcp_data(self, mcp_data: Dict[str, Any]) -> str:
        """Fill company profile template with actual MCP data."""
        csv_path = os.path.join(self.database_dir, "nvidia_company_profile.csv")
        timestamp = datetime.now().isoformat()
        
        # Field mapping from MCP data to CSV fields
        field_mapping = {
            'Symbol': mcp_data.get('symbol', 'N/A'),
            'Company Name': mcp_data.get('companyName', 'N/A'),
            'CEO': mcp_data.get('ceo', 'N/A'),
            'Sector': mcp_data.get('sector', 'N/A'),
            'Industry': mcp_data.get('industry', 'N/A'),
            'Exchange': mcp_data.get('exchange', 'N/A'),
            'Exchange Full Name': mcp_data.get('exchangeFullName', 'N/A'),
            'Website': mcp_data.get('website', 'N/A'),
            'Full Time Employees': mcp_data.get('fullTimeEmployees', 'N/A'),
            'Market Cap': mcp_data.get('marketCap', 'N/A'),
            'Current Price': mcp_data.get('price', 'N/A'),
            'Currency': mcp_data.get('currency', 'N/A'),
            'Volume': mcp_data.get('volume', 'N/A'),
            'Average Volume': mcp_data.get('averageVolume', 'N/A'),
            'Price Range': mcp_data.get('range', 'N/A'),
            'Beta': mcp_data.get('beta', 'N/A'),
            'IPO Date': mcp_data.get('ipoDate', 'N/A'),
            'Last Dividend': mcp_data.get('lastDividend', 'N/A'),
            'Change': mcp_data.get('change', 'N/A'),
            'Change Percentage': mcp_data.get('changePercentage', 'N/A'),
            'Country': mcp_data.get('country', 'N/A'),
            'State': mcp_data.get('state', 'N/A'),
            'City': mcp_data.get('city', 'N/A'),
            'Address': mcp_data.get('address', 'N/A'),
            'Phone': mcp_data.get('phone', 'N/A'),
            'CUSIP': mcp_data.get('cusip', 'N/A'),
            'ISIN': mcp_data.get('isin', 'N/A'),
            'CIK': mcp_data.get('cik', 'N/A'),
            'Description': mcp_data.get('description', 'N/A')[:500] + '...' if mcp_data.get('description') else 'N/A'
        }
        
        # Create rows with actual data
        headers = ['Field', 'Value', 'Timestamp']
        rows = [[field, value, timestamp] for field, value in field_mapping.items()]
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)
        
        return f"Company profile filled with MCP data at {csv_path} with {len(rows)} fields"
    
    def fill_financial_statements_with_mcp_data(self, income_data: list, balance_data: list, cashflow_data: list) -> str:
        """Fill financial statements template with actual MCP data."""
        csv_path = os.path.join(self.database_dir, "nvidia_financial_statements.csv")
        timestamp = datetime.now().isoformat()
        
        headers = ['Statement_Type', 'Metric', 'Value', 'Period', 'Fiscal_Year', 'Date', 'Timestamp']
        rows = []
        
        # Process Income Statement data (last 3 years)
        for stmt in income_data[:3]:
            period = stmt.get('period', 'FY')
            fiscal_year = stmt.get('fiscalYear', 'N/A')
            date = stmt.get('date', 'N/A')
            
            rows.extend([
                ['Income Statement', 'Revenue', stmt.get('revenue', 'N/A'), period, fiscal_year, date, timestamp],
                ['Income Statement', 'Gross Profit', stmt.get('grossProfit', 'N/A'), period, fiscal_year, date, timestamp],
                ['Income Statement', 'Operating Income', stmt.get('operatingIncome', 'N/A'), period, fiscal_year, date, timestamp],
                ['Income Statement', 'Net Income', stmt.get('netIncome', 'N/A'), period, fiscal_year, date, timestamp],
                ['Income Statement', 'EPS', stmt.get('eps', 'N/A'), period, fiscal_year, date, timestamp],
                ['Income Statement', 'EPS Diluted', stmt.get('epsDiluted', 'N/A'), period, fiscal_year, date, timestamp],
                ['Income Statement', 'EBITDA', stmt.get('ebitda', 'N/A'), period, fiscal_year, date, timestamp],
                ['Income Statement', 'R&D Expenses', stmt.get('researchAndDevelopmentExpenses', 'N/A'), period, fiscal_year, date, timestamp]
            ])
        
        # Process Balance Sheet data (last 3 years)
        for stmt in balance_data[:3]:
            period = stmt.get('period', 'FY')
            fiscal_year = stmt.get('fiscalYear', 'N/A')
            date = stmt.get('date', 'N/A')
            
            rows.extend([
                ['Balance Sheet', 'Total Assets', stmt.get('totalAssets', 'N/A'), period, fiscal_year, date, timestamp],
                ['Balance Sheet', 'Total Liabilities', stmt.get('totalLiabilities', 'N/A'), period, fiscal_year, date, timestamp],
                ['Balance Sheet', 'Total Equity', stmt.get('totalEquity', 'N/A'), period, fiscal_year, date, timestamp],
                ['Balance Sheet', 'Cash and Cash Equivalents', stmt.get('cashAndCashEquivalents', 'N/A'), period, fiscal_year, date, timestamp],
                ['Balance Sheet', 'Total Debt', stmt.get('totalDebt', 'N/A'), period, fiscal_year, date, timestamp],
                ['Balance Sheet', 'Inventory', stmt.get('inventory', 'N/A'), period, fiscal_year, date, timestamp],
                ['Balance Sheet', 'Accounts Receivables', stmt.get('accountsReceivables', 'N/A'), period, fiscal_year, date, timestamp]
            ])
        
        # Process Cash Flow data (last 3 years)
        for stmt in cashflow_data[:3]:
            period = stmt.get('period', 'FY')
            fiscal_year = stmt.get('fiscalYear', 'N/A')
            date = stmt.get('date', 'N/A')
            
            rows.extend([
                ['Cash Flow', 'Operating Cash Flow', stmt.get('operatingCashFlow', 'N/A'), period, fiscal_year, date, timestamp],
                ['Cash Flow', 'Free Cash Flow', stmt.get('freeCashFlow', 'N/A'), period, fiscal_year, date, timestamp],
                ['Cash Flow', 'Capital Expenditure', stmt.get('capitalExpenditure', 'N/A'), period, fiscal_year, date, timestamp],
                ['Cash Flow', 'Net Income', stmt.get('netIncome', 'N/A'), period, fiscal_year, date, timestamp],
                ['Cash Flow', 'Dividends Paid', stmt.get('commonDividendsPaid', 'N/A'), period, fiscal_year, date, timestamp]
            ])
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)
        
        return f"Financial statements filled with MCP data at {csv_path} with {len(rows)} metrics"
    
    def get_template_status(self) -> str:
        """Get status of CSV templates and data."""
        files_info = []
        
        csv_files = ['nvidia_company_profile.csv', 'nvidia_financial_statements.csv']
        
        for filename in csv_files:
            filepath = os.path.join(self.database_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as file:
                    rows = sum(1 for _ in file) - 1  # Subtract header row
                    # Check if it's still a template (contains [MCP_DATA])
                    file.seek(0)
                    content = file.read()
                    if '[MCP_DATA]' in content:
                        files_info.append(f"📝 {filename}: Template created ({rows} rows) - NEEDS MCP DATA")
                    else:
                        files_info.append(f"✅ {filename}: Filled with data ({rows} rows)")
            else:
                files_info.append(f"❌ {filename}: Not created yet")
        
        return f"CSV Template Status:\\n" + "\\n".join(files_info)