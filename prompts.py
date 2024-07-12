# LangChain 프롬프트 템플릿을 정의

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

class RequestParam(BaseModel):
    속성: str = Field(description="요청 파라미터의 속성 이름")
    설명: str = Field(description="요청 파라미터의 설명")
    필수여부: str = Field(description="요청 파라미터의 필수 여부 (필수, 선택, 조건부 필수)")

class RequestParamList(BaseModel):
    params: List[RequestParam] = Field(description="요청 파라미터 목록")

class ResponseStructure(BaseModel):
    속성: str = Field(description="응답 구조의 속성 이름")
    설명: str = Field(description="응답 구조의 설명")

class ResponseStructureList(BaseModel):
    structures: List[ResponseStructure] = Field(description="응답 구조 목록")

class IntegrationAPI(BaseModel):
    제공자: str = Field(description="외부 API의 제공자")
    명칭: str = Field(description="외부 API의 명칭")
    식별자: str = Field(description="외부 API의 식별자")

class IntegrationAPIList(BaseModel):
    apis: List[IntegrationAPI] = Field(description="List of integrated external APIs")
    
# JSON 출력 파서
request_parser = JsonOutputParser(pydantic_object=RequestParamList)
response_parser = JsonOutputParser(pydantic_object=ResponseStructureList)
integration_api_parser = JsonOutputParser(pydantic_object=IntegrationAPIList)


request_prompt_template = PromptTemplate(
    template="""
Analyze the provided source code to determine the request parameters. Include all possible fields based on the query builder and resource collection.

Source code: {source_codes}

Include all possible fields based on the query builder and resource collection.
params: 속성, 설명, 필수여부

Describe without direct code references. Write in Korean. Return the result in JSON format.
{format_instructions}
""",
    input_variables=["source_codes"],
    partial_variables={"format_instructions": request_parser.get_format_instructions()}
)

response_prompt_template = PromptTemplate(
    template="""
Analyze the provided source code to determine the response body structure. Include all possible fields based on the resource collection.

Source code: {source_codes}

Include all possible fields based on the query builder and resource collection.
body: 속성, 설명

Describe without direct code references. Write in Korean. Return the result in JSON format.
{format_instructions}
""",
    input_variables=["source_codes"],
    partial_variables={"format_instructions": response_parser.get_format_instructions()}
)

processing_details_prompt_template = PromptTemplate.from_template("""
Analyze the provided source code and briefly describe the processing details.

Source code: {source_codes}

Describe without direct code references. Do not use markdown format. Write in Korean. Be sure to include the following details:
- Functionality it provides
- Data received as input and data returned as output
- A brief explanation of the internal logic
- Details on sorting and pagination
""")

integration_apis_prompt_template = PromptTemplate(
    template="""
Analyze the provided source code and list any external APIs it integrates with.

Source code: {source_codes}

List all integrated external APIs.
apis: 제공자, 명칭, 식별자

Describe without direct code references. Write in Korean. Return the result in JSON format.
{format_instructions}
""",
    input_variables=["source_codes"],
    partial_variables={"format_instructions": integration_api_parser.get_format_instructions()}
)