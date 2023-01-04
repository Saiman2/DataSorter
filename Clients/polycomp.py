from Helpers import Requests
from Helpers import DB
from Helpers import Files
from datetime import datetime


# ToDo This will only insert/update categories/products from the api should we think of way to delete/hide items no longer apear in the api data
class Polycomp:
    url = 'http://api.polycomp.bg/service/data/v1/'
    headers = {
        "Authorization": 'WSSE profile="UsernameToken"',
        'X-WSSE': 'UsernameToken Username="d.petrov",'
                  'PasswordDigest="F396C3B74762B1FEE69B10ABB875139B",'
                  'Nonce = "FDFD123123",'
                  'Created = "2009-06-01T09:00:00Z"'
                  'ApiCode = "121212222…"'
    }

    def __init__(self, *args, **kwargs):
        self.logging = args[0]
        self.db = DB.Connection(*args)
        self.request = Requests.Requests(self.headers, *args, *kwargs)
        self.files = Files.Files(*args)
        print(self.request.get(self.url + 'vendors/test'))
        exit()

    def run(self):
        pass
    #
    # def insert_product(self, product_detail, netcost_cat_id):
    #     pass
    #
    # def handle_category(self, product_categories):
    #     pass
    #
    # def check_if_netcost_category_exists(self, name, ):
    #     pass
    #
    # def insert_category(self, cat, parent_id=None):
    #     pass
    #
    # def get_vali_category(self, product_categories):
    #     pass
