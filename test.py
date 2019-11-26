import json

import requests

from googletrans import Translator

#
# translator = Translator(service_urls=['translate.google.com.tr'])
# text = translator.translate('iyi geceler', dest='ru').text
# print(text)

data = {
    'categories': [62, 63],
    'user_id': 1
}

url = 'http://127.0.0.1:8000/api/v1/admin/document/brands/'
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
r = requests.post(url,
                  data=json.dumps(data), headers=headers)
print(r.status_code)