import requests
from strategy.controllers.convert_data.convert import ConvertData

def auth(identifier, password, url_http):
    data = {
        "identifier": identifier,
        "password": password
    }
    return ConvertData.convert_to_json(
        data=requests.post(url=url_http, data=data).content)