import requests

class HTTPRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint='', params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lanza una excepción si hay un error en la solicitud
        return response.text

    def post(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.text

    def put(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, data=data)
        response.raise_for_status()
        return response.text