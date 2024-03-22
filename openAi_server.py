import openai
import os
from dotenv import load_dotenv

def ai_server():
    # .env 파일에서 환경 변수 불러오기
    load_dotenv()

    # GPT_API_KEY 환경 변수에서 API 키 가져오기
    api_key = os.environ["GPT_API_KEY"]
    openai.api_key = api_key

    # 질문에 대한 대답을 openai에 단답형으로 만들게 하는 질문설정 (핵심 질문 뒤에 붙이세요)
    asked = (" When you recommend clothes, recommend tops, bottoms, hats, outerwear, and shoes. "
             "Also, define each in one word only. For example, tshirts, jeans, cap.. ")

    # ChatGPT API를 사용하여 대화 생성
    response = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0125:personal:test01:95Q5lRy9",  # id가 아닌 모델 이름 기입요망
        messages=[
            {"role": "system",
             "content": "a delicate clothes coordinator who recommends clothes according to the weather"},
            {"role": "user", "content": "Please recommend clothes to wear on broken clouds days in -10 degrees"}
        ]
    )

    # 응답 출력
    print(response)
    print("=============")
    print(response.choices[0].message.content)

    return response.choices[0].message.content
