import requests
from bs4 import BeautifulSoup as bs
from seleniumCrawling import get_clothes_detail_info


def get_clothes_list(shopping_mall_url):
    try:
        response = requests.get(shopping_mall_url)
        response.raise_for_status()
        soup = bs(response.content, 'html.parser')
        element_array = soup.select('#searchList > li:nth-child(n) > div.li_inner')
        product_data_list = []
        for element in element_array:
            small_img_element = element.select_one("div.li_inner > div.list_img > a > img")
            small_img = small_img_element['data-original'] if small_img_element else None
            a_find = element.select_one("div.li_inner > div.list_img > a")
            path = a_find['href'] if a_find else None
            url = f"https:{path}" if path else None
            brand = element.select_one("div.li_inner > div.article_info > p.item_title > a").get_text(strip=True)
            product_name = element.select_one("div.li_inner > div.article_info > p.list_info > a")['title']

            # 제품 상세정보 수집
            clothes_detail_info = get_clothes_detail_info(url)
            big_img = clothes_detail_info['big_img']
            thickness = clothes_detail_info['thickness']
            season = clothes_detail_info['season']
            size = clothes_detail_info['size']
            price = clothes_detail_info['price']

            product_data_list.append({
                'small_img': small_img,
                'brand': brand,
                'product_name': product_name,
                'big_img': big_img,
                'thickness': thickness,
                'season': season,
                'size': size,
                'price': price
            })

        return product_data_list

    except Exception as e:
        print("제품 리스트 불러오기 실패 : ", e)
