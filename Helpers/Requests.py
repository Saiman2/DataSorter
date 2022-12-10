import requests


class Requests:
    name = None
    headers = {
        'vali': {
            "Authorization": "Bearer rmphSfgH7ehBEP5SocwlKblvIvuv44ncHEOs8kNtm64wSoSEuGoHIzXGKBD2",
            'Accept': 'application/json'
        }
    }

    def __init__(self, *args, **kwargs):
        self.name = args[0]
        self.logging = args[1]

    def get(self, url, headers=None):
        if not headers:
            headers = self.headers[self.name]
            # print(headers)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            self.logging.error('Url: ' + url +' Code: ' + str(response.status_code))
            return False

        return response.json()

