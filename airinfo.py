from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# API 설정
AIR_QUALITY_API_URL = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
KAKAO_REST_API_KEY = 'e5e14ace39b80119810abeed55f01e71'  # 카카오 REST API 키
API_KEY = 'LryfSU7qm7CctuENGzZz3OsjE8IaeFgrvYz0vKU6kJJ7/A02eKZ5QsyGPEN+uzrYUK3j91RcHEhsFnjlq/0Pjg=='  # 대기질 API 키 (인코딩된 키)

def get_air_quality_data():
    params = {
        'serviceKey': API_KEY,
        'returnType': 'json',
        'numOfRows': 10,
        'pageNo': 1,
        'sidoName': '서울',
        'ver': '1.0'
    }
    response = requests.get(AIR_QUALITY_API_URL, params=params)

    # 상태 코드와 응답 출력
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 200:
        try:
            return response.json()  # JSON 파싱
        except ValueError:
            print("Error decoding JSON:", response.text)
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# 카카오 REST API로 주소를 위도와 경도로 변환하는 함수
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

@app.route('/')
def index():
    return render_template('airinfo.html')

@app.route('/get_data')
def get_data():
    air_quality_data = get_air_quality_data()
    if air_quality_data:
        items = air_quality_data['response']['body']['items']
        locations = []
        for item in items:
            # 주소와 미세먼지 정보를 사용
            address = f"{item['stationName']}, 서울"
            coordinates = get_coordinates_by_address(address)
            if coordinates:
                locations.append({
                    "stationName": item['stationName'],
                    "pm10Value": item['pm10Value'],
                    "lat": coordinates['lat'],
                    "lng": coordinates['lng']
                })
        return jsonify(locations)
    else:
        return jsonify({"error": "Failed to fetch air quality data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
