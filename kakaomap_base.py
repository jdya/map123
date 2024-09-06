from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# 카카오 REST API 키
KAKAO_REST_API_KEY = 'e5e14ace39b80119810abeed55f01e71'

# 카카오 REST API로 도로명 주소를 위도와 경도로 변환하는 함수
def get_coordinates_by_address(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {
        "Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"  # REST API 키를 헤더에 포함
    }
    params = {
        "query": address  # 검색할 도로명 주소
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['documents']:
            # 위도와 경도를 추출
            x = data['documents'][0]['x']  # 경도
            y = data['documents'][0]['y']  # 위도
            return {"lat": float(y), "lng": float(x)}
    return None

@app.route('/')
def index():
    return render_template('kakaomap_base.html')

# 예시로 데이터 반환 (도로명 주소를 좌표로 변환)
@app.route('/get_coordinates/<address>')
def get_coordinates(address):
    coordinates = get_coordinates_by_address(address)
    if coordinates:
        return jsonify(coordinates)
    else:
        return jsonify({"error": "Failed to fetch coordinates"}), 500

if __name__ == '__main__':
    app.run(debug=True)
