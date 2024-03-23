import os
from flask import Flask, request, make_response, jsonify
import requests
import json
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
headerToken = os.getenv("HEADERTOKEN")


@app.route('/sendmessage', methods=['POST'])
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

@app.route('/clothesAi', methods=['POST'])
def handled_clothesAi():
    if request.method == 'POST':
        cloth_list = request.json

        # openai 응답 메시지
        message = ai_server(cloth_list)

        try:
            response = requests.post(spring_server_url, data=message)
            if response.status_code == 200:
                return jsonify({"message" : "send success"})
            else:
                return jsonify({"message" : "send fail"})
        except requests.exceptions.RequestException as e:
            return jsonify({'error': 'Failed to send data: ' + str(e)})



if __name__ == '__main__':
    app.run(host=os.getenv("HOST_IP"), port=os.getenv("PORT"), debug=True)
