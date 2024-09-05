from flask import Flask

# Flask 애플리케이션 생성
app = Flask(__name__)

# 라우트 설정 (홈 페이지)
@app.route('/')
def hello_world():
    return 'Hello, World!'  # 웹 브라우저에서 이 메시지를 출력

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
