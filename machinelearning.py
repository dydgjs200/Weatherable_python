import requests
from bs4 import BeautifulSoup as bs


# ----------------------------------머신러닝 스타일 학습이미지 수집----------------------------------
# 스트릿 남성 상의 (무신사 검색)
# page = requests.get("https://www.musinsa.com/search/musinsa/goods?q=%EC%8A%A4%ED%8A%B8%EB%A6%BF+%EB%82%A8%EC%84%B1+%EC%83%81%EC%9D%98&list_kind=small&sortCode=pop&sub_sort=&page=1&display_cnt=0&saleGoods=&includeSoldOut=&setupGoods=&popular=&category1DepthCode=&category2DepthCodes=&category3DepthCodes=&selectedFilters=&category1DepthName=&category2DepthName=&brandIds=&price=&colorCodes=&contentType=&styleTypes=&includeKeywords=&excludeKeywords=&originalYn=N&tags=&campaignId=&serviceType=&eventType=&type=&season=&measure=&openFilterLayout=N&selectedOrderMeasure=&shoeSizeOption=&groupSale=&d_cat_cd=&attribute=&plusDeliveryYn=")
# 스트릿 여상 상의 (무신사 검색)
page = requests.get("https://www.musinsa.com/search/musinsa/goods?q=%EC%8A%A4%ED%8A%B8%EB%A6%BF+%EC%97%AC%EC%84%B1+%EC%83%81%EC%9D%98&list_kind=small&sortCode=pop&sub_sort=&page=1&display_cnt=0&saleGoods=&includeSoldOut=&setupGoods=&popular=&category1DepthCode=&category2DepthCodes=&category3DepthCodes=&selectedFilters=&category1DepthName=&category2DepthName=&brandIds=&price=&colorCodes=&contentType=&styleTypes=&includeKeywords=&excludeKeywords=&originalYn=N&tags=&campaignId=&serviceType=&eventType=&type=&season=&measure=&openFilterLayout=N&selectedOrderMeasure=&shoeSizeOption=&groupSale=&d_cat_cd=&attribute=&plusDeliveryYn=")
soup = bs(page.text, "html.parser")
elements = soup.select('#searchList > li:nth-child(n) > div.li_inner')
smallImgs = soup.select('#searchList > li:nth-child(n) > div.li_inner > div.list_img > a > img')
smallImgArray = []

for index, element in enumerate(smallImgs):
    # print('https:'+element.attrs['data-original'])
    smallImgArray.append('https:'+element.attrs['data-original'])

print(smallImgArray)
print(len(smallImgArray))
