import requests
from flask import Flask, render_template, jsonify
from xml.etree import ElementTree as ET

app = Flask(__name__)

# 성범죄자 알림e API URL
API_URL = "http://api.sexoffender.go.kr/openapi/SOCitysStats/"

# API 호출 후 JSON 데이터로 변환
def get_api_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        xml_data = response.text
        root = ET.fromstring(xml_data)
        locations = []
        
        # 시도별 성범죄자 데이터를 리스트에 저장
        for city in root.findall("City"):
            city_name = city.find("city-name").text
            city_count = city.find("city-count").text
            coordinates = get_coordinates_by_city(city_name)
            if coordinates:
                locations.append({
                    "name": city_name,
                    "count": city_count,
                    "lat": coordinates["lat"],
                    "lng": coordinates["lng"]
                })
        return locations
    return []

# 시도별 위도와 경도 설정 (수동으로 좌표 설정)
def get_coordinates_by_city(city_name):
    coordinates = {
        "서울특별시": {"lat": 37.5665, "lng": 126.9780},
        "부산광역시": {"lat": 35.1796, "lng": 129.0756},
        "대구광역시": {"lat": 35.8714, "lng": 128.6014},
        "인천광역시": {"lat": 37.4563, "lng": 126.7052},
        "광주광역시": {"lat": 35.1595, "lng": 126.8526},
        "대전광역시": {"lat": 36.3504, "lng": 127.3845},
        "울산광역시": {"lat": 35.5393, "lng": 129.3114},
        "세종특별자치시": {"lat": 36.4875, "lng": 127.2816},
        "경기도": {"lat": 37.4138, "lng": 127.5183},
        "강원특별자치도": {"lat": 37.5558, "lng": 128.2093},
        "충청북도": {"lat": 36.6354, "lng": 127.4916},
        "충청남도": {"lat": 36.5184, "lng": 126.8000},
        "전라북도": {"lat": 35.8200, "lng": 127.1088},
        "전라남도": {"lat": 34.8679, "lng": 126.9910},
        "경상북도": {"lat": 36.4919, "lng": 128.8889},
        "경상남도": {"lat": 35.4606, "lng": 128.2132},
        "제주특별자치도": {"lat": 33.4996, "lng": 126.5312},
        "기타": {"lat": 36.5, "lng": 127.5}
    }
    return coordinates.get(city_name, None)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/locations')
def locations():
    data = get_api_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
