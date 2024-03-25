import os
from flask import Flask, request, jsonify
import requests
import time
from dotenv import load_dotenv
from flask_cors import CORS
from openAi_server import ai_server

import classification_OneFile as onefile

app = Flask(__name__)
CORS(app, supports_credentials=True)
load_dotenv()

# onefile은 하나의 파일만 검색함

# 전송할 스프링 서버 주소값
next_server_url = os.getenv("NEXT_SERVER_URL")
spring_server_url = os.getenv("SPRING_SERVER_URL")

@app.route('/closet/styleai', methods=['POST'])
def handle_request():
    if request.method == 'POST':

        start_time = time.time()

        data = request.form.to_dict()

        resDict = {}

        print("data > ", data)

        for key, value in data.items():
            img_url, style, score = onefile.predict_cloth(key, value)
            resDict[style] = score

        print(resDict)

        # 서버에 보내기
        try:
            end_time = time.time()
            print(f"Total execution time: {end_time - start_time}")

            return resDict
        except Exception as e:
            print("Error while sending data to Spring server:", str(e))
            return 'Error while sending data to Spring server!'

@app.route('/recommend/cloth', methods=['GET'])
def handled_clothesAi():
    if request.method == 'GET':
        accessToken = request.headers["Authorization"]      # jwt 토큰
        cloth_list = request.json

        # openai 응답 메시지
        response = ai_server(cloth_list)
        params = {"response" : response}
        print(response)

        try:
            headers = {'Authorization': accessToken}       # jwt 토큰 헤더 설정
            message = requests.get(spring_server_url, params=params, headers=headers)
            if message.status_code == 200:
                print("rrr >", message.text)
                return jsonify({"message" : "send success"})
            else:
                print("rrr >" , message.text)
                return jsonify({"message" : "send fail"})
        except requests.exceptions.RequestException as e:
            return jsonify({'error': 'Failed to send data: ' + str(e)})

@app.route('/dddd', methods=["GET"])
def handle_weather():
    if request.method == "GET":
        ans = request.json

    return ans

if __name__ == '__main__':
    app.run(host=os.getenv("HOST_IP"), port=os.getenv("PORT"), debug=True)
