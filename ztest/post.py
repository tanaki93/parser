import json

import requests

# headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
#
# url = 'http://127.0.0.1:8000/api/v1/main/order/'
# myobj = {
#     'phone': '+996700161629',
#     'price': '300',
#     'address': 'ul. Frunze 22',
#     'lat': 42.872008,
#     'lng': 74.590787,
#     'items': [{'food_id': 4,
#                'amount': 1,
#                'price': 150},
#               {'food_id': 5,
#                'amount': 1,
#                'price': 150},
#               ],
# }
#
# x = requests.post(url, data=json.dumps(myobj), headers=headers)
#
# print(x.text)

from decimal import Decimal

from yandex_geocoder import Client


client = Client("9c36b1b7-d684-47cb-975e-77d6277ebfdb")

coordinates = client.coordinates("Москва Льва Толстого 16")
assert coordinates == (Decimal("37.587093"), Decimal("55.733969"))

address = client.address(Decimal("37.587093"), Decimal("55.733969"))
assert address == "Россия, Москва, улица Льва Толстого, 16"
