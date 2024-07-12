# 요청 파라미터와 응답 구조를 추출

import asyncio
import json
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from prompts import (
    request_prompt_template, 
    response_prompt_template, 
    processing_details_prompt_template, 
    integration_apis_prompt_template,
    request_parser,
    response_parser,
    integration_api_parser
)

# 환경 변수 로드
load_dotenv()

llm = ChatOpenAI(
    temperature=0.1,
    model_name="gpt-4o"
)

def create_message(prompt_template, input_data: dict):
    return prompt_template.format(**input_data)

# RunnableLambda 인스턴스 생성
request_runnable = RunnableLambda(lambda input_data: request_parser.parse(
    StrOutputParser().parse(
        llm.invoke(create_message(request_prompt_template, input_data)).content
    )
))
response_runnable = RunnableLambda(lambda input_data: response_parser.parse(
    StrOutputParser().parse(
        llm.invoke(create_message(response_prompt_template, input_data)).content
    )
))
processing_details_runnable = RunnableLambda(lambda input_data: 
    llm.invoke(create_message(processing_details_prompt_template, input_data)).content.strip()
)
integration_apis_runnable = RunnableLambda(lambda input_data: integration_api_parser.parse(
    StrOutputParser().parse(
        llm.invoke(create_message(integration_apis_prompt_template, input_data)).content
    )
))

async def extract_parameters(source_codes):
    source_codes_str = json.dumps(source_codes, indent=4)
    input_data = {"source_codes": source_codes_str}
    
    request_params = request_runnable.invoke(input_data)
    response_structure = response_runnable.invoke(input_data)
    processing_details = processing_details_runnable.invoke(input_data)
    integration_apis = integration_apis_runnable.invoke(input_data)

    return json.dumps(request_params, ensure_ascii=False), json.dumps(response_structure, ensure_ascii=False), processing_details, json.dumps(integration_apis, ensure_ascii=False)
