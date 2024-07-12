# OpenAPI Markdown 문서를 생성

import json

def generate_markdown(request_params, response_structure, processing_details, integration_apis):
    request_params_json = json.loads(request_params)
    response_structure_json = json.loads(response_structure)
    integration_apis_json = json.loads(integration_apis)

    request_table = "| 속성 | 설명 | 필수여부 |\n|------|------|--------|\n"
    for param in request_params_json['params']:
        request_table += f"| {param['속성']} | {param['설명']} | {param['필수여부']} |\n"

    response_table = "| 속성 | 설명 |\n|------|------|\n"
    for structure in response_structure_json['structures']:
        response_table += f"| {structure['속성']} | {structure['설명']} |\n"

    if integration_apis_json['apis'] and len(integration_apis_json['apis']) > 0:
        integration_table = ""
        for api in integration_apis_json['apis']:
            integration_table += f"{api['제공자']} > {api['명칭']} ({api['식별자']})\n"
    else:
        integration_table = "없음"

    final_document = f"""
## 매니저 관리
https://admin.tworldfriends.co.kr/supervisor/managers

## 처리내용
{processing_details}

## 요청
{request_table}

## 응답
{response_table}

## 연동 API
{integration_table}
"""

    with open("output/api_documentation.md", "w") as md_file:
        md_file.write(final_document)
