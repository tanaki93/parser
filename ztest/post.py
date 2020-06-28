import json

import requests

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

url = 'https://tamak.pixelkalpak.com/api/v1/code/'
myobj = {
    'code': '9286',
}

x = requests.get(url, data=json.dumps(myobj), headers=headers)

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
