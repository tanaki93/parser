import json

import requests
#
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
#
# url = 'http://188.120.242.218:8089/api/v1/main/checkout/'
# myobj = {
#     'products_price': '1000',
#     'total_price': '1000',
#     'shipping_price': '1000',
#     'products': [{'product_id': 75227,
#                   'size_id': 157,
#                   'amount': 1,
#                   'price': 1000}, ],
# }
#
# x = requests.post(url, data=json.dumps(myobj), headers=headers)
#
# print(x.text)

import requests


def telegram_bot_sendtext(bot_message):
    url = 'https://api.telegram.org/bot1097337743:AAHQ4aOXQrTsDO3ZlzHVeUcjA77Ys_4VlMg/getUpdates'
    x = requests.get(url)
    print(x.text)
    n = json.loads(x.text)
    l = []
    for i in n['result']:
        chat = i['message']['chat']['id']
        if chat not in l:
            l.append(chat)

    print(l)
    for j in l:
        bot_chatID = '%s'%j
        bot_token = '1097337743:AAHQ4aOXQrTsDO3ZlzHVeUcjA77Ys_4VlMg'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=HTML&text=' + bot_message
        response = requests.get(send_text)
        print(response.json())

    return ''


text = '<b>Заказ № 536546576234365 оплачен</b>\n <a href=\"https://admin.izishop.kg/orders/112\">Ссылка: https://admin.izishop.kg/orders/112</a>\n <i>Сумма заказа: 2200</i>'
telegram_bot_sendtext(text)
