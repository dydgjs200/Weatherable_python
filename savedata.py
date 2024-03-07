from pymongo import MongoClient

# mongoDB URL
mongodb_URL = "mongodb+srv://Yongheon:GO8EwDBUlGrj6ND2@weatherable.hlkyrfr.mongodb.net/"

client = MongoClient(mongodb_URL)

print(client.list_database_names())

db = client['weatherable']

collection = db['clothes']

# from webcrawling import get_clothes_list
# product_list_url = 'https://www.musinsa.com/categories/item/001005'
# product_list = get_clothes_list(product_list_url)

data = {"major_category": "Top", "middle_category": "Sweat_shirt", "price": 59900, "color": "네이비", "thickness": "보통",
        "product_name": "SMALL CENTER 맨투맨 (STMSTD-0015)", "brand": "1989스탠다드",
        "small_img": "https://image.msscdn.net/images/goods_img/20221220/2990274/2990274_16947549126831_125.jpg",
        "big_img": "https://image.msscdn.net/images/goods_img/20221220/2990274/2990274_16947549126831_500.jpg"}

clothes = db.clothes
data_id = clothes.insert_one(data).inserted_id
print(data_id)