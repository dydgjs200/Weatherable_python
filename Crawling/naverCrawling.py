import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import requests

chrome_options = Options()
chrome_options.add_argument("--headless")  # Headless 모드 활성화
chrome_options.add_argument("--disable-gpu")  # GPU 사용 안 함 (가속화 불가)
chrome_options.add_argument("--no-sandbox")  # 보안 Sandbox 모드 끄기

for i in range(1, 2):
    # 주소 수정요망
    crawling_link = f"https://search.shopping.naver.com/search/all?adQuery=%ED%8F%AC%EB%A9%80%20%EC%83%81%EC%9D%98&frm=NVSCTAB&origQuery=%ED%8F%AC%EB%A9%80%20%EC%83%81%EC%9D%98&pagingIndex={i}&pagingSize=40&productSet=total&query=%ED%8F%AC%EB%A9%80%20%EC%83%81%EC%9D%98&sort=rel&timestamp=&viewType=list"
    driver = webdriver.Chrome(service=Service('C:\chromedriver-win64\chromedriver.exe'), options=chrome_options)
    driver.get(crawling_link)
    wait = WebDriverWait(driver, 10)

    # 로컬 디렉토리 경로 (수정 요망)
    save_dir = r"C:\Users\user\Desktop\Code\project\weatherable\머신러닝학습이미지\네이버\포멀"

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        goods_list = soup.select('#content > div.style_content__xWg5l > div.basicList_list_basis__uNBZx > div > div:nth-child(n) > div > div > div.product_img_area__cUrko > div > a > img')
        print(goods_list)
        print(len(goods_list))


        # 이미지 다운로드
        # for index, img_element in enumerate(img_elements1):
        #     img_uri = img_element.get_attribute('src')
        #     print(index, img_uri)
        #     img_data = requests.get(img_uri).content
        #     with open(os.path.join(save_dir, f'image_{i}_{index}.jpg'), 'wb') as f:
        #         f.write(img_data)
        #
        # print(f"{i} page 이미지 다운로드 완료")

    except Exception as e:
        continue

