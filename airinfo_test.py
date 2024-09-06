import requests

# 대기질 정보 조회 함수
def get_air_quality_data():
    AIR_QUALITY_API_URL = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
    API_KEY = 'LryfSU7qm7CctuENGzZz3OsjE8IaeFgrvYz0vKU6kJJ7/A02eKZ5QsyGPEN+uzrYUK3j91RcHEhsFnjlq/0Pjg=='
    
    params = {
        'serviceKey': API_KEY,
        'returnType': 'json',  # 'xml' 또는 'json'
        'numOfRows': 100,
        'pageNo': 1,
        'sidoName': '서울',  # 시도 이름
        'ver': '1.0'
    }

    # API 요청
    response = requests.get(AIR_QUALITY_API_URL, params=params)
    
    # 상태 코드 출력
    print(f"Status Code: {response.status_code}")
    
    # 응답 내용 출력 (텍스트)
    print(f"Response Text: {response.text}")
    
    # 상태 코드가 200인 경우에만 JSON으로 변환 시도
    if response.status_code == 200:
        try:
            return response.json()  # JSON 파싱
        except ValueError:
            print("Error decoding JSON.")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# 함수 호출 및 데이터 출력
air_quality_data = get_air_quality_data()

if air_quality_data:
    print("Air Quality Data:", air_quality_data)
else:
    print("Failed to retrieve air quality data.")
