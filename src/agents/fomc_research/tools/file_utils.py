import os
import io
import base64
import logging
import pdfplumber
import requests

logger = logging.getLogger(__name__)

TMP_DIR = os.path.join(os.path.dirname(__file__), "tmp")
os.makedirs(TMP_DIR, exist_ok=True)

async def download_pdf_to_local(url: str, filename: str) -> str:
    """Downloads a PDF file to the local `tmp` directory and returns the full path."""
    try:
        logger.info("Downloading %s", url)
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        full_path = os.path.join(TMP_DIR, filename)
        with open(full_path, "wb") as f:
            f.write(response.content)

        logger.info("Downloaded to %s", full_path)
        return full_path

    except requests.exceptions.RequestException as e:
        logger.error("Error downloading file from URL: %s", e)
        return ""


async def extract_text_from_pdf_local(filepath: str) -> str:
    """Extracts text from a local PDF file."""
    try:
        logger.info("Extracting text from %s", filepath)
        text = ""
        with open(filepath, "rb") as f:
            with pdfplumber.open(f) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()
        return text
    except Exception as e:
        logger.error("Error reading PDF: %s", e)
        return ""
