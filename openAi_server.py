import openai
import os
from dotenv import load_dotenv

def ai_server(cloth_list):
    # .env 파일에서 환경 변수 불러오기
    load_dotenv()

    # GPT_API_KEY 환경 변수에서 API 키 가져오기
    api_key = os.environ["GPT_API_KEY"]
    gpt_model = os.environ["GPT_MODEL_NAME"]
    openai.api_key = api_key

    # 질문 전 가정하기 (핵심 질문 앞에 붙이세요)
    after_asked = "나는 아래의 옷들을 갖고 있어.\n"
    for major_category in cloth_list:
        after_asked += f"{major_category} : "
        for item in cloth_list[major_category]:
            after_asked += f"{item[0]} --{item[1]}--, "
        after_asked += "\n"

    print(after_asked)

    # 질문에 대한 대답을 openai에 단답형으로 만들게 하는 질문설정 (핵심 질문 뒤에 붙이세요)
    before_asked = ("상의, 하의, 아우터, 신발, 모자로 나누어서 각 종류 당 1개씩 추천해줘. 만약 각 부위의 아이템이 없다면 없음으로 출력해줘라."
                    "또한, 답변은 부위 : 아이템이름으로만 출력해줘. 출력 시, -- 뒤의 부분은 제거해라.")

    # ChatGPT API를 사용하여 대화 생성
    response = openai.ChatCompletion.create(
        model=gpt_model,  # id가 아닌 모델 이름 기입요망
        messages=[
            # {"role": "system",
            #  "content": "a delicate clothes coordinator who recommends clothes according to the weather"},
            # {"role": "user", "content": "Please recommend clothes to wear on broken clouds days in -10 degrees. please speak korean."}

            {"role": "system",
            "content": "옷 코디네이터"},
            {"role": "user", "content": after_asked + "기온 : 1도, 날씨 : 화창 / 이러한 조건일 때 보유한 옷의 종류를 보고 옷을 추천해줘 \n" + before_asked}
        ]
    )

    # 응답 출력
    print(response)
    print("=============")

    # print(response.choices[0].message.content)

    return response.choices[0].message.content
