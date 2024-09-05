import requests
from xml.etree import ElementTree as ET

# API URL
api_url = "http://api.sexoffender.go.kr/openapi/SOCitysStats/"

# API 요청 보내기
response = requests.get(api_url)

# 상태 코드 확인
if response.status_code == 200:
    print("API 호출 성공")
    
    # 응답 데이터를 텍스트로 출력 (XML 형식)
    xml_data = response.text
    print("응답 XML 데이터:")
    print(xml_data)
    
    # XML 데이터를 파싱하여 시도별 성범죄자 수 출력
    root = ET.fromstring(xml_data)
    
    print("\n시도별 성범죄자 수:")
    for city in root.findall("City"):
        city_name = city.find("city-name").text
        city_count = city.find("city-count").text
        print(f"{city_name}: {city_count}명")
else:
    print(f"API 호출 실패. 상태 코드: {response.status_code}")
