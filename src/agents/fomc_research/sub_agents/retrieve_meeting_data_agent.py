# Copyright 2025 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0

"""Retrieve meeting data sub-agent for FOMC Research Agent"""

from typing import List, Dict
import os

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from ..agent import MODEL
from ..shared_libraries.callbacks import rate_limit_callback
from ..tools.fetch_page import fetch_page_tool
from ..tools.file_utils import download_pdf_to_local, extract_text_from_pdf_local
from . import retrieve_meeting_data_agent_prompt
from .extract_page_data_agent import ExtractPageDataAgent


async def retrieve_statement_texts(
    statement_urls: List[str],
    filenames: List[str]
) -> Dict[str, str]:
    """
    Downloads multiple statement PDFs, extracts text, deletes the files.

    Args:
        statement_urls: List of PDF URLs to download.
        filenames: Corresponding local filenames to save temporarily.

    Returns:
        Dictionary {filename: extracted_text}
    """
    result = {}
    temp_paths = []

    try:
        for url, name in zip(statement_urls, filenames):
            pdf_path = await download_pdf_to_local(url, name)
            temp_paths.append(pdf_path)

            if not pdf_path:
                result[name] = "PDF download failed."
                continue

            extracted_text = await extract_text_from_pdf_local(pdf_path)
            result[name] = extracted_text or "PDF text extraction failed."

        return result

    except Exception as e:
        return {"error": str(e)}

    finally:
        for path in temp_paths:
            try:
                if path and os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                print(f"[WARN] Failed to delete {path}: {e}")

RetrieveMeetingDataAgent = Agent(
    model=MODEL,
    name="retrieve_meeting_data_agent",
    description="Retrieve data about a Fed meeting from the Fed website",
    instruction=retrieve_meeting_data_agent_prompt.PROMPT,
    tools=[
        fetch_page_tool,
        AgentTool(ExtractPageDataAgent),
        retrieve_statement_texts,
    ],
    sub_agents=[],
    before_model_callback=rate_limit_callback,
)
