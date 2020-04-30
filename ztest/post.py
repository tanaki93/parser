import json

import requests

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

url = 'http://127.0.0.1:8000/api/v1/vk/'
myobj = {
    'access_token': '6727f01f67177eb0fedd42726f60b69543ee623b2a644e7a966ff3627fec9d88fc1b756ab160c561c7d95'
}

x = requests.post(url, data=json.dumps(myobj), headers=headers)

print(x.text)

# from decimal import Decimal
#
# from yandex_geocoder import Client
#
#
# client = Client("9c36b1b7-d684-47cb-975e-77d6277ebfdb")
#
# coordinates = client.coordinates("Москва Льва Толстого 16")
# assert coordinates == (Decimal("37.587093"), Decimal("55.733969"))
#
# address = client.address(Decimal("37.587093"), Decimal("55.733969"))
# assert address == "Россия, Москва, улица Льва Толстого, 16"
