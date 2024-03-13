from flask import Flask, request
import requests
from multiprocessing import Pool
import json
import time
import classification_cloth_model as pred

app = Flask(__name__)

# 전송할 스프링 서버 주소값
spring_server_url = 'http://localhost:8080/sendmessage'

def predict_cloth_wrapper(args):
    classification, url = args
    return pred.predict_cloth(classification, url)

@app.route('/sendmessage', methods=['POST'])
def handle_request():
    if request.method == 'POST':
        start_time = time.time()
        data = request.json
        resDict = {}

        # Extract classification and URLs from the received data
        predictions_input = []
        for classification, urls in data.items():
            for url in urls:
                predictions_input.append((classification, url))

        # 멀티프로세스 처리 -> 실험을 3 부분으로 해서 3개로 프로세스 나눔
        with Pool(processes=3) as pool:
            results = pool.map(predict_cloth_wrapper, predictions_input)

        # 딕셔너리에 결과값 저장
        for result in results:
            for k, v in result.items():
                if k in resDict:
                    resDict[k].append(v)
                else:
                    resDict[k] = [v]

        # 서버에 보내기
        try:
            response = requests.post(spring_server_url, json=json.dumps(resDict, ensure_ascii=False))
            print("Response from Spring server:", response.text)

            end_time = time.time()
            print(f"Total execution time: {end_time - start_time}")

            return 'POST request received successfully and forwarded to Spring server!'
        except Exception as e:
            print("Error while sending data to Spring server:", str(e))
            return 'Error while sending data to Spring server!'

if __name__ == '__main__':
    app.run(port=5000)
