import os
from flask import Flask, request
import requests
import json
import time
from dotenv import load_dotenv

import classification_OneFile as onefile

app = Flask(__name__)
load_dotenv()

# onefile은 하나의 파일만 검색함

# 전송할 스프링 서버 주소값
next_server_url = os.getenv("NEXT_SERVER_URL")
headerToken = os.getenv("HEADERTOKEN")

@app.route('/sendmessage', methods=['POST'])
def handle_request():
    if request.method == 'POST':
        start_time = time.time()

        # "multipart/form-data" 형식의 데이터를 읽기 위해 request.form 사용
        data = request.form.to_dict()

        resDict = {}

        print("data > ", data)

        for key, value in data.items():
            img_url, style, score = onefile.predict_cloth(key, value)
            resDict[style] = score

        # resDict[style] = score
        print(resDict)

        # 서버에 보내기
        try:
            headers = {"Authorization": headerToken}
            response = requests.post(next_server_url, json=json.dumps(resDict, ensure_ascii=False), headers=headers)
            print("Response from Spring server:", response.text, response.status_code)

            end_time = time.time()
            print(f"Total execution time: {end_time - start_time}")

            return 'POST request received successfully and forwarded to Spring server!'
        except Exception as e:
            print("Error while sending data to Spring server:", str(e))
            return 'Error while sending data to Spring server!'


if __name__ == '__main__':
    app.run(host=os.getenv("HOST_IP"), port=os.getenv("PORT"))
