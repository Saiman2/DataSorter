from Helpers import Requests
from Helpers import DB
from Helpers import Files
from datetime import datetime


# ToDo This will only insert/update categories/products from the api should we think of way to delete/hide items no longer apear in the api data
class Vali:
    url = 'https://www.vali.bg/api/v1/'
    headers = {
        "Authorization": "Bearer rmphSfgH7ehBEP5SocwlKblvIvuv44ncHEOs8kNtm64wSoSEuGoHIzXGKBD2",
        'Accept': 'application/json'
    }

    def __init__(self, *args, **kwargs):
        self.logging = args[0]
        # self.logging.warning('This will get logged to a fileeeee')
        self.db = DB.Connection(*args)
        self.request = Requests.Requests('vali', self.headers, *args, *kwargs)
        self.files = Files.Files(*args)
        response = self.request.get(self.url + 'categories')
        if response:
            self.categories = response.json()

    def run(self):
        # products = self.request.get(self.url + 'products')
        products = []
        response = self.request.get(self.url + 'products')
        if response:
            products = response.json()
        # products = [
        #     {'id': 143, 'idWF': 6160, 'reference_number': 'HDD-SATA3-1000WD-BLUE', 'manufacturer_id': 130, 'status': 1,
        #      'price_client': 77.45, 'price_partner': 68.09, 'show': True, 'categories': [{'id': 496}]}
        # ]
        # print(products)
        i = 0
        for product in products:
            # print(product)
            # exit()
            i = i + 1
            if i == 15:
                exit()
            netcost_cat_id = self.handle_category(product['categories'])
            if netcost_cat_id is False:
                # ToDo decide what to do if we fail to assign category to products
                continue

            product_detail = None
            response = self.request.get(self.url + 'product/' + str(product['id']) + '/full')
            if response:
                product_detail = response.json()

            if not product_detail:
                self.logging.info('Product details not found for product_id:' + str(product['id']))

            print('netcost_cat_id')
            print(netcost_cat_id)

            self.insert_product(product_detail, netcost_cat_id)
            # exit()
            # print(product_detail)

    def insert_product(self, product_detail, netcost_cat_id):
        print('product_detail')
        print(product_detail)
        # return True
        # exit()
        name = None
        slug = None
        for item in product_detail['name']:
            if item['language_code'] == 'bg':
                name = item['text'].replace(',', "")
            elif item['language_code'] == 'en':
                slug = item['text'].replace(" ", "-").replace(',', "")

        if name is None:
            self.logging.error('Vali insert_product no bg name product_detail: ' + str(product_detail) + ' Slug: ' + str(slug))
            return False
        is_netcost_product = self.db.fetch_one('SELECT * FROM products WHERE name=%s', (name,))
        # print('is_netcost_product')
        # print(is_netcost_product)
        # exit()

        # Temp
        # is_netcost_product = None
        if is_netcost_product is not None:
            print('is_netcost_product')
            print(is_netcost_product)
            self.files.upload_image(product_detail['images'], is_netcost_product[0])
            return True

        description = None
        for item in product_detail['description']:
            if item['language_code'] == 'bg':
                description = item['text']

        if len(description) == 0:
            description = name

        # ToDo Which is discount
        end_price = product_detail['price_client']
        recommended_price = product_detail['price_client']
        dealer_price = product_detail['price_partner']

        active = 0
        if product_detail['show']:
            active = 1

        # ToDo should we validate if this is all completed i saw there is no desc sometimes
        netcost_tuple = (name, slug, description, end_price, recommended_price, dealer_price, netcost_cat_id, active, datetime.now(), datetime.now(),)
        # print(netcost_tuple)

        sql = "INSERT INTO products (name,slug,description,end_price,recommended_price,dealer_price,category_id,active,created_at,updated_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        inserted = self.db.insert_return_id(sql, netcost_tuple)
        if inserted and product_detail['images']:
            self.files.upload_image(product_detail['images'], inserted)
        print('inserted')
        print(inserted)
        # if product_detail['id'] == 219:
        #     exit()

    def handle_category(self, product_categories):
        vali_cat = self.get_vali_category(product_categories)
        if vali_cat is False:
            self.logging.error(
                'Vali category not found in all vali categories product_categories: ' + str(product_categories))
            return False
        netcost_cat = self.check_if_netcost_category_exists(vali_cat['name'])
        if netcost_cat is False:
            netcost_parent_id = None
            if vali_cat['parent'] != 0:
                # print('handeParent')
                vali_parent_cat = self.get_vali_category(vali_cat['parent'])
                if vali_parent_cat is not False:
                    netcost_parent_cat = self.check_if_netcost_category_exists(vali_parent_cat['name'])
                    # print('netcost_parent_cat')
                    # print(netcost_parent_cat)
                    if netcost_parent_cat is False:
                        is_inserted = self.insert_category(vali_parent_cat)
                        netcost_parent_id = is_inserted
                    else:
                        netcost_parent_id = netcost_parent_cat
                else:
                    self.logging.error(
                        'Vali category with parent not found in all vali categories id(parent): ' + str(vali_cat['parent']))

            # print('netcost_parent_id')
            # print(netcost_parent_id)
            is_inserted = self.insert_category(vali_cat, netcost_parent_id)
            return is_inserted

        return netcost_cat

    def check_if_netcost_category_exists(self, name, ):
        if type(name) == list:
            for transName in name:
                if transName['language_code'] == 'bg':
                    is_category = self.db.fetch_one('SELECT * FROM products_categories WHERE name=%s', (transName['text'],))
                    if is_category is None:
                        return False
                    return is_category[0]
        is_category = self.db.fetch_one('SELECT * FROM products_categories WHERE name=%s', (name,))

        if is_category == None:
            return False
        return is_category[0]

    def insert_category(self, cat, parent_id=None):
        name = None
        slug = None
        for trans_names in cat['name']:
            if trans_names['language_code'] == 'bg':
                name = trans_names['text']
            elif trans_names['language_code'] == 'en':
                slug = trans_names['text'].replace(" ", "-")
        sql = "INSERT INTO products_categories (name,slug,parent_id,created_at,updated_at) VALUES(%s,%s,%s,%s,%s)"
        inserted = self.db.insert_return_id(sql, (name, slug, parent_id, datetime.now(), datetime.now(),))
        return inserted

    def get_vali_category(self, product_categories):

        if type(product_categories) == list:
            listproduct_categories = []
            for prodCat in product_categories:
                listproduct_categories.append(prodCat['id'])
        else:
            listproduct_categories = [product_categories]
        for cat in self.categories:
            if cat['id'] in listproduct_categories:
                return cat
        return False
