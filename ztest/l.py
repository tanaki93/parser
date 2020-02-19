import json
from random import randint

import requests


def main():
    client_id = '170000005'
    oid = ''
    amount = 10.0
    okurl = 'http://104.248.31.32/success/'
    failurl = 'http://104.248.31.32/fail/'
    transaction_type = 'Auth'
    instalment = '0'
    rnd = randint(1000, 9999)
    storekey = 'TEST1234'
    storetype = '3d_Pay_Hosting'
    currency = '417'
    lang = 'ru'

    plaintext = client_id + oid + str(amount) + okurl + failurl + transaction_type + instalment + str(rnd) + storekey
    import base64
    import hashlib
    hash = base64.b64encode(hashlib.sha1(str.encode(plaintext)).digest())
    hash = (hash.decode("utf-8"))
    data = {
        'clientid': client_id,
        'storetype': storetype,
        'hash': hash,
        'islemtipi': transaction_type,
        'amount': amount,
        'currency': currency,
        'oid': oid,
        'rnd': rnd,
        'okUrl': okurl,
        'failUrl': failurl,
        'lang': lang,
        'taksit': instalment,
    }
    url = 'https://entegrasyon.asseco-see.com.tr/fim/est3Dgate'
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.text)


if __name__ == '__main__':
    main()
