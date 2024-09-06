import requests

# 성범죄자 도로명 주소 정보 API 설정
SEX_OFFENDER_API_URL = 'http://apis.data.go.kr/1383000/sais/SexualAbuseNoticeRoadnameAddrService/getSexualAbuseNoticeRoadnameAddrList'

# Encoding된 API 인증키
API_KEY = 'LryfSU7qm7CctuENGzZz3OsjE8IaeFgrvYz0vKU6kJJ7%2FA02eKZ5QsyGPEN%2BuzrYUK3j91RcHEhsFnjlq%2F0Pjg%3D%3D'

# 요청 매개변수 설정
params = {
    'serviceKey': API_KEY,
    'pageNo': 1,
    'numOfRows': 10,
    '_type': 'json'  # json 형식으로 응답을 받기 위해 설정
}

# API 요청
response = requests.get(SEX_OFFENDER_API_URL, params=params)

# 응답 확인
if response.status_code == 200:
    try:
        print(response.json())
    except ValueError:
        print("Error decoding JSON:", response.text)
else:
    print(f"Error {response.status_code}: {response.text}")
