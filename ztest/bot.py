import requests


def main():
    text = '<b>Заказ № %s оплачен</b>\n<a href=\"https://admin.izishop.kg/orders/%s\">Ссылка на заказ </a>\n <b>Сумма заказа: %s</b>' % (
        21332452345, 2, 100)
    bot_chatID = '%s' % 735923723
    bot_token = '1097337743:AAHQ4aOXQrTsDO3ZlzHVeUcjA77Ys_4VlMg'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=HTML&text=' + text
    response = requests.get(send_text)
    print(response.json())

if __name__ == '__main__':
    main()