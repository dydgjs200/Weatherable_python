import os
import requests
from bs4 import BeautifulSoup as bs

for i in range(1, 11):
    # 주소 수정요망
    crawling_link = f"https://www.musinsa.com/app/codimap/lists?style_type=chic&tag_no=&brand=&display_cnt=60&list_kind=big&sort=date&page={i}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    page = requests.get(crawling_link, headers=headers)
    soup = bs(page.text, "html.parser")
    smallImgs = soup.select(
        'body > div.wrap > div.right_area > form > div.right_contents.hover_box > div > ul > li:nth-child(n) > div.style-list-item__thumbnail > a > div > img')
    # 로컬 디렉토리 경로 (수정 요망)
    save_dir = r"C:\Users\user\Desktop\Code\project\weatherable\머신러닝학습이미지\스타일\시크"

    # print(smallImgs)
    # 디렉토리가 없을 경우 생성
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for index, img in enumerate(smallImgs):
        try:
            # img_url = 'https:' + img.attrs['src']
            img_url = 'https:' + img.attrs['data-original']
            print(index, img_url)
            img_data = requests.get(img_url).content
            # 이미지를 로컬 디렉토리에 저장
            with open(os.path.join(save_dir, f'image_{i}_{index}.jpg'), 'wb') as f:
                f.write(img_data)

        except Exception as e:
            continue

    print(f"{i} page 이미지 다운로드 완료")
