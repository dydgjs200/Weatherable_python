from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # Headless 모드 활성화
chrome_options.add_argument("--disable-gpu")  # GPU 사용 안 함 (가속화 불가)
chrome_options.add_argument("--no-sandbox")  # 보안 Sandbox 모드 끄기


def get_clothes_detail_info(clothes_detail_url):
    print("get_clothes_detail_info 실행")
    # Chrome 드라이버 생성
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(clothes_detail_url)
    # time.sleep(1)
    wait = WebDriverWait(driver, 10)

    # 제품 이미지 (500x600)
    try:
        big_img_element = driver.find_element(By.CSS_SELECTOR,
                                              "#root > div.product-detail__sc-8631sn-0.gJskhq > div.product-detail__sc-8631sn-1.fPAiGD > div.product-detail__sc-8631sn-3.jKqPJk > div.product-detail__sc-p62agb-0.daKJsk > div > img")
        big_img = big_img_element.get_attribute('src')
        # print(big_img)
    except NoSuchElementException:
        # print("해당 요소가 존재하지 않습니다")
        pass

    # 제품연관 해시태그 (설명)
    try:
        hash_tags_elements = driver.find_elements(By.CSS_SELECTOR,
                                                  "#root > div.product-detail__sc-8631sn-0.gJskhq > div.product-detail__sc-8631sn-1.fPAiGD > div.product-detail__sc-8631sn-4.goIKhx > div.product-detail__sc-achptn-0.bHXxTQ > div > a:nth-child(n)")
        hash_tags = []
        for hash_tags_element in hash_tags_elements:
            hash_tags.append(hash_tags_element.get_attribute('title'))
        # print(hash_tags)
    except NoSuchElementException:
        # print("해당 요소가 존재하지 않습니다")
        pass

    # 제품 두께
    try:
        thickness_element = driver.find_element(By.CSS_SELECTOR,
                                                "#root > div.product-detail__sc-8631sn-0.gJskhq > div.product-detail__sc-8631sn-1.fPAiGD > div.product-detail__sc-8631sn-3.jKqPJk > div.product-detail__sc-17fds8k-0.PpQGA > table > tbody > tr:nth-child(5) > td.product-detail__sc-17fds8k-5.gpXliU")
        thickness = thickness_element.text
        # print(thickness)
    except NoSuchElementException:
        thickness = None
        # print(thickness)

    # 제품 착용권장 계절
    try:
        season_elements = driver.find_elements(By.CSS_SELECTOR,
                                           "#root > div.product-detail__sc-8631sn-0.gJskhq > div.product-detail__sc-8631sn-1.fPAiGD > div.product-detail__sc-8631sn-3.jKqPJk > div.product-detail__sc-17fds8k-0.PpQGA > table > tbody > tr:nth-child(6) > td.product-detail__sc-17fds8k-5.gpXliU")
        seasons = []
        for season_element in season_elements:
            seasons.append(season_element.text)
        # print(seasons)
    except NoSuchElementException:
        seasons = None
        # print(seasons)

    # 제품 사이즈
    try:
        size_elements = driver.find_elements(By.CSS_SELECTOR,
                                             "#root > div.product-detail__sc-8631sn-0.gJskhq > div.product-detail__sc-8631sn-1.fPAiGD > div.product-detail__sc-8631sn-3.jKqPJk > div.product-detail__sc-swak4b-0.KLfjI > table > tbody > tr:nth-child(n+2) > th")
        sizes = []
        for size_element in size_elements:
            size_text = size_element.text.strip('[]')
            sizes.append(size_text)
        # print(sizes)
    except NoSuchElementException:
        # print("해당 요소가 존재하지 않습니다")
        pass

    # 제품 가격
    try:
        price_element = driver.find_element(By.CSS_SELECTOR, "#root > div.product-detail__sc-8631sn-0.gJskhq > div.product-detail__sc-8631sn-1.fPAiGD > div.product-detail__sc-8631sn-4.goIKhx > div.product-detail__sc-w5wkld-0.hgCYZm > div.product-detail__sc-1p1ulhg-0.jEclp > ul > li:nth-child(1) > div.product-detail__sc-1p1ulhg-6.fKNtEN > span")
        price = int(price_element.text.replace(',', '').replace('원', ''))
    except NoSuchElementException:
        pass

    product_detail_info = {}
    product_detail_info['big_img'] = big_img
    product_detail_info['thickness'] = thickness
    product_detail_info['season'] = seasons
    product_detail_info['size'] = sizes
    product_detail_info['price'] = price
    return product_detail_info
