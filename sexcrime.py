from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# 카카오 REST API 키
KAKAO_REST_API_KEY = 'e5e14ace39b80119810abeed55f01e71'

# 성범죄자 도로명 주소 정보 API 설정
SEX_OFFENDER_API_URL = 'http://apis.data.go.kr/1383000/sais/SexualAbuseNoticeRoadnameAddrService/getSexualAbuseNoticeRoadnameAddrList'
API_KEY = 'LryfSU7qm7CctuENGzZz3OsjE8IaeFgrvYz0vKU6kJJ7%2FA02eKZ5QsyGPEN%2BuzrYUK3j91RcHEhsFnjlq%2F0Pjg%3D%3D'

# 카카오 REST API로 도로명 주소를 위도와 경도로 변환하는 함수
def get_coordinates_by_address(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {
        "Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"
    }
    params = {
        "query": address
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['documents']:
            x = data['documents'][0]['x']  # 경도
            y = data['documents'][0]['y']  # 위도
            return {"lat": float(y), "lng": float(x)}
    return None

# 성범죄자 도로명 주소 정보 API 호출 함수
def get_sexual_offender_data():
    params = {
        'serviceKey': API_KEY,  # Encoding된 API 키
        'numOfRows': 10,        # 한 페이지 결과 수
        'pageNo': 1,            # 페이지 번호
        '_type': 'json'         # 응답 타입 JSON
    }

    response = requests.get(SEX_OFFENDER_API_URL, params=params)
    
    # 응답 상태 코드 확인
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            # JSON 파싱이 실패한 경우 오류 메시지 출력
            print("Error decoding JSON:", response.text)
            return None
    else:
        # 상태 코드가 200이 아닌 경우 오류 메시지 출력
        print(f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}")
        return None

@app.route('/')
def index():
    return render_template('sexcrime.html')

@app.route('/get_data')
def get_data():
    data = get_sexual_offender_data()
    if data:
        items = data['response']['body']['items']['item']
        locations = []
        for item in items:
            address = f"{item['ctpvNm']} {item['sggNm']} {item['umdNm']} {item['roadNm']}"
            coordinates = get_coordinates_by_address(address)
            if coordinates:
                locations.append({
                    "address": address,
                    "lat": coordinates['lat'],
                    "lng": coordinates['lng'],
                    "rfrncAddr": item['rfrncAddr'],
                    "ctpvNm": item['ctpvNm'],
                    "sggNm": item['sggNm'],
                    "umdNm": item['umdNm'],
                    "roadNm": item['roadNm'],
                    "bmno": item['bmno'],
                    "bsno": item['bsno']
                })
        return jsonify(locations)
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
