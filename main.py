import json
import asyncio
from extractor import extract_parameters
from generator import generate_markdown
from dotenv import load_dotenv
from langchain_teddynote import logging

with open('source_codes.json', 'r') as f:
    source_codes = json.load(f)

async def main():
    load_dotenv()
    logging.langsmith("langchainDocTool")
    request_params, response_structure, processing_details, integration_apis = await extract_parameters(source_codes)
    generate_markdown(request_params, response_structure, processing_details, integration_apis)

if __name__ == "__main__":
    asyncio.run(main())
