import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 성범죄자 알림e API URL
API_URL = "http://api.sexoffender.go.kr/openapi/SOCitysStats/"

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/locations')
def get_locations():
    # API 요청 보내기
    response = requests.get(API_URL)

    # 응답 출력 (디버깅용)
    print(response.text)


    # API 응답이 성공적이면 XML 데이터를 JSON으로 변환
    if response.status_code == 200:
        data = response.text  # XML 데이터를 텍스트로 받음
        parsed_data = parse_xml_to_json(data)  # XML을 JSON 형식으로 변환
        return jsonify(parsed_data)  # JSON 형식으로 반환
    else:
        return jsonify({"error": "Unable to fetch data"}), 500

def parse_xml_to_json(xml_data):
    from xml.etree import ElementTree as ET

    root = ET.fromstring(xml_data)
    locations = []

    for city in root.findall("City"):
        city_name = city.find("city-name").text
        city_count = city.find("city-count").text
        # 위도와 경도는 수동으로 정의 (대한민국 각 지역의 중앙 좌표)
        coords = get_coordinates_by_city(city_name)
        locations.append({
            "name": city_name,
            "count": city_count,
            "lat": coords["lat"],
            "lng": coords["lng"]
        })

    return locations

def get_coordinates_by_city(city_name):
    # 각 시도별 좌표 (위도, 경도)
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
        "기타": {"lat": 36.5, "lng": 127.5}  # 기타 지역
    }

    return coordinates.get(city_name, {"lat": 36.5, "lng": 127.5})  # 기본값으로 대한민국 중앙 좌표
