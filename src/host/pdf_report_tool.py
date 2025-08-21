from google.adk.tools import FunctionTool
import os
import pandas as pd
from datetime import datetime

def load_csv_data():
    """Load CSV data from the database directory"""
    try:
        # Get current file's directory and navigate to CSV files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        csv_dir = os.path.join(project_root, "agents", "financial_modeling", "database")
        
        company_profile_path = os.path.join(csv_dir, "nvidia_company_profile.csv")
        financial_statements_path = os.path.join(csv_dir, "nvidia_financial_statements.csv")
        
        company_data = None
        financial_data = None
        
        if os.path.exists(company_profile_path):
            company_data = pd.read_csv(company_profile_path)
        
        if os.path.exists(financial_statements_path):
            financial_data = pd.read_csv(financial_statements_path)
            
        return company_data, financial_data
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        return None, None

def create_investment_markdown_report(
    company_research_data: str,
    fomc_research_data: str,
    investment_analysis: str
) -> str:
    """Create comprehensive markdown investment report from research data.
    
    Args:
        company_research_data: Output from company search agent
        fomc_research_data: Output from FOMC research agent  
        investment_analysis: Final investment recommendation and analysis
        
    Returns:
        str: Path to created markdown file
    """
    try:
        # Load CSV data from database
        company_data, financial_data = load_csv_data()
        
        # Create reports directory if it doesn't exist
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        # Generate markdown filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        md_filename = f"investment_research_report_{timestamp}.md"
        md_path = os.path.join(reports_dir, md_filename)
        
        # Build markdown content
        content = []
        
        # Title and header
        content.append("# Investment Research Report")
        content.append("")
        
        # Add company name if available
        if company_data is not None and not company_data.empty:
            company_name = company_data[company_data['Field'] == 'Company Name']['Value'].iloc[0] if not company_data[company_data['Field'] == 'Company Name'].empty else "Company Analysis"
            content.append(f"## **{company_name}** Financial Analysis")
        
        content.append("")
        content.append(f"*Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}*")
        content.append("")
        content.append("```")
        content.append("AI-Powered Comprehensive Financial Analysis")
        content.append("Integrating Real-time Data & Research")
        content.append("```")
        content.append("")
        content.append("---")
        content.append("")
        
        # Executive Summary
        content.append("## Executive Summary")
        content.append("")
        
        # Add company overview from CSV data
        if company_data is not None and not company_data.empty:
            company_name = company_data[company_data['Field'] == 'Company Name']['Value'].iloc[0] if not company_data[company_data['Field'] == 'Company Name'].empty else "Unknown"
            sector = company_data[company_data['Field'] == 'Sector']['Value'].iloc[0] if not company_data[company_data['Field'] == 'Sector'].empty else "Unknown"
            market_cap = company_data[company_data['Field'] == 'Market Cap']['Value'].iloc[0] if not company_data[company_data['Field'] == 'Market Cap'].empty else "Unknown"
            current_price = company_data[company_data['Field'] == 'Current Price']['Value'].iloc[0] if not company_data[company_data['Field'] == 'Current Price'].empty else "Unknown"
            
            content.append(f"> **Company:** {company_name} ({sector} sector)")
            content.append(f"> **Market Cap:** ${float(market_cap):,.0f} | **Current Price:** ${current_price}")
            content.append("")
        
        # Extract key points from investment analysis for executive summary
        exec_summary = investment_analysis[:1200] + "..." if len(investment_analysis) > 1200 else investment_analysis
        content.append(exec_summary)
        content.append("")
        
        # Investment Analysis Section
        content.append("## Investment Analysis")
        content.append("")
        
        # Split long text into paragraphs for better formatting
        analysis_paragraphs = investment_analysis.split('\n\n')
        for para in analysis_paragraphs:
            if para.strip():
                content.append(para.strip())
                content.append("")
        
        content.append("---")
        content.append("")
        
        # Financial Data Section
        content.append("## Financial Data Analysis")
        content.append("")
        
        # Add financial statements table from CSV
        if financial_data is not None and not financial_data.empty:
            content.append("### Key Financial Metrics (3-Year Comparison)")
            content.append("")
            
            # Filter for latest 3 years of income statement data
            income_data = financial_data[financial_data['Statement_Type'] == 'Income Statement']
            
            if not income_data.empty:
                # Create markdown table
                content.append("| Metric | FY 2025 | FY 2024 | FY 2023 |")
                content.append("|--------|---------|---------|---------|")
                
                metrics = ['Revenue', 'Gross Profit', 'Operating Income', 'Net Income', 'EPS Diluted']
                for metric in metrics:
                    row = [metric]
                    for year in [2025, 2024, 2023]:
                        value = income_data[(income_data['Metric'] == metric) & (income_data['Fiscal_Year'] == year)]
                        if not value.empty:
                            val = value['Value'].iloc[0]
                            if metric == 'EPS Diluted':
                                row.append(f"${val}")
                            else:
                                row.append(f"${float(val)/1e9:.1f}B" if float(val) > 1e9 else f"${float(val)/1e6:.1f}M")
                        else:
                            row.append("N/A")
                    content.append("| " + " | ".join(row) + " |")
                
                content.append("")
        
        content.append("---")
        content.append("")
        
        # Company Research Section
        content.append("## Company Research & Analysis")
        content.append("")
        
        # Add company profile from CSV data
        if company_data is not None and not company_data.empty:
            content.append("### Company Profile")
            content.append("")
            
            # Create company profile table
            content.append("| Attribute | Value |")
            content.append("|-----------|-------|")
            
            key_fields = ['Symbol', 'CEO', 'Industry', 'Full Time Employees', 'Website', 'Exchange', 'IPO Date']
            
            for field in key_fields:
                value_row = company_data[company_data['Field'] == field]
                if not value_row.empty:
                    value = value_row['Value'].iloc[0]
                    if field == 'Full Time Employees':
                        value = f"{int(float(value)):,}"
                    content.append(f"| {field} | {value} |")
            
            content.append("")
        
        company_paragraphs = company_research_data.split('\n\n')
        for para in company_paragraphs:
            if para.strip():
                content.append(para.strip())
                content.append("")
        
        content.append("---")
        content.append("")
        
        # FOMC/Macro Analysis Section  
        content.append("## Macroeconomic & Federal Reserve Analysis")
        content.append("")
        
        fomc_paragraphs = fomc_research_data.split('\n\n')
        for para in fomc_paragraphs:
            if para.strip():
                content.append(para.strip())
                content.append("")
        
        # Conclusion
        content.append("---")
        content.append("")
        content.append("## Conclusion & Recommendations")
        content.append("")
        content.append(
            "This comprehensive research report integrates financial data analysis, "
            "competitive intelligence, and macroeconomic factors to provide a complete "
            "investment perspective. The analysis considers multiple data sources and "
            "quantitative models to deliver actionable investment recommendations."
        )
        content.append("")
        
        content.append("### Data Sources & Methodology")
        content.append("")
        content.append("- **Financial Data:** MCP Financial Modeling Prep API (CSV Database)")
        content.append("- **Company Research:** EXA Search Engine Intelligence")
        content.append("- **Federal Reserve Data:** FOMC Meeting Minutes & Economic Projections")
        content.append("- **AI Analysis:** Gemini 2.5 Pro Language Model")
        content.append("- **Report Generation:** Automated Markdown Creation System")
        content.append("- **Data Integration:** CSV files with real-time financial metrics")
        content.append("")
        
        # Add data freshness information
        if company_data is not None and not company_data.empty:
            timestamp = company_data['Timestamp'].iloc[0] if 'Timestamp' in company_data.columns else "Unknown"
            content.append(f"`Data Last Updated: {timestamp}`")
            content.append("")
        
        # Write markdown file
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        return f"Investment research markdown report created successfully at: {md_path}\nFile type: Professional markdown document\nIncludes: Executive Summary with CSV data, Financial Analysis Tables, Company Profile, Investment Analysis, Company Research, FOMC Analysis, Conclusions\nData Sources: CSV files from database + Agent memory content"
        
    except Exception as e:
        return f"Error creating markdown report: {str(e)}"

# Create FunctionTool instance
create_markdown_report_tool = FunctionTool(create_investment_markdown_report)