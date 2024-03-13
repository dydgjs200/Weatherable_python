import os
import requests
from bs4 import BeautifulSoup as bs

## 무신사 크롤링

for i in range(1, 16):
    # 주소 수정요망
    crawling_link = f"https://www.musinsa.com/search/musinsa/goods?q=%EC%8A%A4%ED%8F%AC%ED%8B%B0&list_kind=small&sortCode=pop&page={i}&display_cnt=0&saleGoods=false&includeSoldOut=false&setupGoods=false&popular=false&category1DepthCode=005&selectedFilters=%EC%8B%A0%EB%B0%9C%3A005%3Acategory1DepthCode&category1DepthName=%EC%8B%A0%EB%B0%9C&originalYn=N&openFilterLayout=N"
    page = requests.get(crawling_link)
    soup = bs(page.text, "html.parser")
    smallImgs = soup.select('#searchList > li:nth-child(n) > div.li_inner > div.list_img > a > img')

    # 로컬 디렉토리 경로 (수정 요망)
    save_dir = "C:/Users/user/Desktop/crawling/스포티_신발"

    # 디렉토리가 없을 경우 생성
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for index, img in enumerate(smallImgs):
        img_url = 'https:' + img.attrs['data-original']
        img_data = requests.get(img_url).content
        # 이미지를 로컬 디렉토리에 저장
        with open(os.path.join(save_dir, f'image_{i}_{index}.jpg'), 'wb') as f:
            f.write(img_data)

    print(f"{i} page 이미지 다운로드 완료")
