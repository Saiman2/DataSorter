import requests


class Requests:
    headers = None

    def __init__(self, *args):
        self.headers = args[0]
        self.logging = args[1]

    def get(self, url, headers=None, stream=None):
        if not headers and self.headers:
            headers = self.headers
        # print(headers)
        response = requests.get(url, headers=headers, stream=stream)
        if response.status_code != 200:
            self.logging.error('Url: ' + url + ' Code: ' + str(response.status_code))
            return False

        return response
