import requests
from PIL import Image, ImageOps
import numpy as np
from keras.models import load_model
from io import BytesIO  # BytesIO를 임포트합니다.

import os

def predict_cloth(classification, img_url):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # 현재 스크립트 파일의 경로
    current_dir = os.path.dirname(__file__)
    model_dir = os.path.join(current_dir, 'KerasModels')

    predict_file_path = {
        "Top": ["keras_model_top.h5", "labels_top.txt"],
        "Bottom": ["keras_model_bottom.h5", "labels_bottom.txt"],
        "Outer": ["keras_model_outer.h5", "labels_outer.txt"]
    }

    # 부위에 따른 로드하는 분류모델 로드
    model_file = predict_file_path[classification][0]
    model_path = os.path.join(model_dir, model_file)
    model = load_model(model_path, compile=False)

    # 라벨 로드
    label_file = predict_file_path[classification][1]
    label_path = os.path.join(model_dir, label_file)
    class_names = open(label_path, "rt", encoding="UTF-8").readlines()

    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    response = requests.get(img_url)
    image_data = response.content

    # 이미지 열기
    image = Image.open(BytesIO(image_data)).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    # print("Class:", class_name[2:], "Confidence Score:", confidence_score)

    # image open은 호출될 때 마다 메모리에 적재되므로 del을 통해 해제할 필요가 있음
    del image

    # return {img_url: [class_name[2:], str(confidence_score)]}
    style_list = {
        "Top" : ["캐주얼 상의\n", "고프고어 상의\n", "포멀 상의\n", "스포티 상의\n", "레트로 상의\n"],
        "Bottom": ["캐주얼 하의\n", "고프코어 하의\n", "포멀 하의\n", "스포티 하의\n", "레트로 하의\n"],
        "Outer": ["캐주얼 아우터\n", "고프코어 아우터\n", "포멀 아우터\n", "스포티 아우터\n", "레트로 아우터\n"],
        "Shoes": ["캐주얼 신발\n", "고프코어 신발\n", "포멀 신발\n", "스포티 신발\n", "레트로 신발\n"],
        "Hat": ["캐주얼 모자\n", "고프코어 모자\n", "포멀 모자\n", "스포티 모자\n", "레트로 모자\n"]
    }

    # score는 float32형이지만, json에서 전달 불가하므로 문자열로 처리
    return img_url, style_list[classification].index(class_name[2:]), str(confidence_score)
    # return img_url, class_name[2:], str(confidence_score)