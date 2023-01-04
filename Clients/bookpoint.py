import json
from Helpers import DB
from Helpers import Files
from datetime import datetime


class BookPoint:

    def __init__(self, *args):
        self.logging = args[0]
        self.db = DB.Connection(*args)
        self.files = Files.Files(*args)

    def run(self):

        # ToDo check if item could have more than one image and if so is the key in changed
        with open('./ToSort/BOOKPOINT/products.json', encoding="utf8") as f:
            data = json.load(f)

        i = 0
        for item in data:
            i = i + 1
            if i == 1000:
                break

            print(self.insert_item(item))
        f.close()
        return True

        # item = {'id': '8', 'isbn': '9789546261472', 'name': 'Кибалион', 'author': 'Тримата Посветени', 'publisher': 'Аратрон', 'price': '9.00', 'publishYear': '2019', 'pages': '144', 'weight': '0', 'cover_type': 'Мекa',
        #         'size': {'width': '13.00', 'height': '20.00'}, 'language': 'Български', 'url': 'http://www.bookpoint.bg/книги/Кибалион-8.htm', 'categories': ['Езотерика и теософия', 'Религия и митология'],
        #         'image': 'http://www.bookpoint.bg/files/mf/books/8_pic_m.jpg',
        #         'description': '„За нас е голямо удоволствие да представим на вниманието на учениците и изследователите на тайните учения тази малка книга, основаваща се върху древното херметично учение. Целта на книгата не е формулирането на някаква специална философия или учение, а по-скоро да даде на учениците една теза за истината и тя да послужи за помирение на различните части от окултното познание, които привидно са противоположни едни на други.\r\n\r\nНамерението ни не е да издигнем нов храм на знанието, а по-скоро да предоставим в ръцете на ученика универсален ключ, с който да може да отвори много вътрешни врати в храма на мистериите, през чиито главни врати той вече е преминал.\r\n\r\nПостарали сме се да ви дадем представа за фундаменталните учения на Кибалион, като сме разкрили работните принципи, така че вие да ги приложите сами. Ако вие сте истински ученик, ще успеете да използвате тези Принципи - ако не сте, трябва да се развиете, тъй като в противен случай херметичното учение ще бъде за вас просто думи.&quot;\r\n\r\nТримата Посветени'}

    def insert_item(self, product_detail):
        # print('product_detail')
        # print(product_detail)
        # print(product_detail['name'])
        is_netcost_product = self.db.fetch_one('SELECT * FROM products WHERE name=%s', (product_detail['name'],))
        # print('is_netcost_product')
        # print(is_netcost_product)
        # exit()

        if is_netcost_product is not None:
            # print('Images')
            # print(product_detail)
            # print(product_detail['image'])
            self.files.upload_images([product_detail['image']], is_netcost_product[0])
            return True
        netcost_cat_id = self.handle_category(product_detail['categories'])

        # NAMING
        name = product_detail['name']
        slug = product_detail['name']
        if name is None:
            self.logging.error('Bookpoint insert_product no name product_detail: ' + str(product_detail))
            name = 'Няма име'
            slug = 'Няма име'

        # PRICING
        dealer_price = float(product_detail['price']) - (25 * float(product_detail['price'])) / 100
        recommended_price = product_detail['price']
        end_price = float(product_detail['price']) + (3 * float(product_detail['price'])) / 100

        netcost_tuple = (name, slug, product_detail['description'],
                         end_price, recommended_price, dealer_price,
                         netcost_cat_id[0], 1, datetime.now(), datetime.now(),)

        sql = "INSERT INTO products (name,slug,description,end_price,recommended_price,dealer_price,category_id,active,created_at,updated_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        inserted = self.db.insert_return_id(sql, netcost_tuple)
        if inserted and product_detail['image']:
            self.files.upload_images([product_detail['image']], inserted)

        if inserted:
            return True
        return False

    def handle_category(self, categories):
        # print(categories)
        # print(len(categories))
        total_categories = len(categories)

        if categories[0] == None:
            return self.insert_categories(['Други'], None)

        if total_categories == 1:
            return self.insert_categories(categories, None)
        if total_categories == 2:
            main_category = categories[total_categories - 1]
            main_category_id = None
            categories.remove(main_category)

            is_main_category = self.db.fetch_one('SELECT * FROM products_categories WHERE name=%s', (main_category,))
            if is_main_category is None:
                sql = "INSERT INTO products_categories (name,slug,parent_id,created_at,updated_at) VALUES(%s,%s,%s,%s,%s)"
                main_category_id = self.db.insert_return_id(sql, (main_category, main_category, None, datetime.now(), datetime.now(),))
            else:
                main_category_id = is_main_category[0]

            if main_category_id is None:
                self.logging.error('No main_category_id: ' + str(main_category_id))
                return False
            return self.insert_categories(categories, main_category_id)

        if total_categories >= 3:
            main_category = categories[total_categories - 1]
            main_category_id = None
            sub_category = categories[total_categories - 2]
            sub_category_id = None
            categories.remove(main_category)
            categories.remove(sub_category)

            is_main_category = self.db.fetch_one('SELECT * FROM products_categories WHERE name=%s', (main_category,))
            if is_main_category is None:
                sql = "INSERT INTO products_categories (name,slug,parent_id,created_at,updated_at) VALUES(%s,%s,%s,%s,%s)"
                main_category_id = self.db.insert_return_id(sql, (main_category, main_category, None, datetime.now(), datetime.now(),))
            else:
                main_category_id = is_main_category[0]

            is_sub_category = self.db.fetch_one('SELECT * FROM products_categories WHERE name=%s', (sub_category,))
            if is_sub_category is None:
                sql = "INSERT INTO products_categories (name,slug,parent_id,created_at,updated_at) VALUES(%s,%s,%s,%s,%s)"
                sub_category_id = self.db.insert_return_id(sql, (sub_category, sub_category, main_category_id, datetime.now(), datetime.now(),))
            else:
                sub_category_id = is_sub_category[0]

            if main_category_id is None and sub_category_id is None:
                self.logging.error('No main or sub cat_id main_category_id: ' + str(main_category_id) + ' sub_category_id: ' + str(sub_category_id))
                return False
            # print('main_category_id')
            # print(main_category_id)
            # print('sub_category_id')
            # print(sub_category_id)
            return self.insert_categories(categories, sub_category_id)

    def insert_categories(self, categories, sub_category_id):
        inserted_categories = []
        for cat in categories:
            # print(cat)
            sub_sub_category_id = None
            is_sub_sub_category = self.db.fetch_one('SELECT * FROM products_categories WHERE name=%s', (cat,))
            if is_sub_sub_category is None:
                sql = "INSERT INTO products_categories (name,slug,parent_id,created_at,updated_at) VALUES(%s,%s,%s,%s,%s)"
                sub_sub_category_id = self.db.insert_return_id(sql, (cat, cat, sub_category_id, datetime.now(), datetime.now(),))
            else:
                sub_sub_category_id = is_sub_sub_category[0]

            if sub_sub_category_id is None:
                self.logging.error('Failed to insert sub sub cat: ' + str(sub_sub_category_id))
                continue
            inserted_categories.append(sub_sub_category_id)
        return inserted_categories
        # example
        # ['Мениджмънт', 'Финанси', 'Икономическа литература', 'Икономика и право']
        # ['Проза', 'Българска литература', 'Художествена литература']
        # ['Книги']
        # [None]
