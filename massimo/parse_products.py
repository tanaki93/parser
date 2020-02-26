#!/usr/bin/env python
# -*- coding: utf-8
import json
import time
from multiprocessing.dummy import Pool
from pprint import pprint
from random import choice

import requests
from bs4 import BeautifulSoup

from koton.constants import PROXIES, USERAGENTS


def get_html(url):
    print(url)
    proxy = {'http': 'http://' + choice(PROXIES)}
    useragent = {'User-Agent': choice(USERAGENTS)}
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_html1(url):
    r = requests.get(url)
    return r.text


def get_categories_from_db(url):
    html = get_html1(url)
    return json.loads(html)


def get_data(context):
    product_dict = {
        'id': context['id']
    }
    cont = {}
    url = context['url']
    category_id = url.split('category_id=')[1]
    colour_id = url.split('?colorId=')[1].split('&category_id=')[0]
    product_id = url.split('%s' % category_id)[1].split('.html')[0][1:]
    product_json_url = 'https://www.massimodutti.com/itxrest/2/catalog/store/34009471/30359503/category/0/product/%s/detail?languageId=-43&appId=2' % product_id
    html = get_html(product_json_url)
    json_data = json.loads(html)
    cont['name'] = json_data['name']
    cont['stock'] = True
    cont['product_id'] = product_id
    cont['product_code'] = product_id
    cont['description'] = json_data['detail']['longDescription']
    static = 'https://static.massimodutti.net/3/photos'
    medias = json_data['detail']['xmedia']
    images = []
    for media in medias:
        if media['colorCode'] == str(colour_id):
            path = static + media['path'] + '/'
            for xmedia in media['xmediaItems'][0]['medias']:
                image = path + xmedia['idMedia'] + '16.jpg?t=' + str(
                    xmedia['timestamp']) + '&impolicy=massimodutti-itxmedium&imwidth=700'
                images.append(image)
        break
    image_text = ''
    for image in images:
        image_text = image_text + image + ' '
    cont['images'] = image_text
    product_sizes = []
    for color in json_data['detail']['colors']:
        if color['id'] == str(colour_id):
            cont['colour'] = color['name']
            product_sizes = color['sizes']
            break
    stock_url = 'https://www.massimodutti.com/itxrest/2/catalog/store/34009471/30359503/product/%s/stock?languageId=-43&appId=2' % product_id
    stock_json = get_html(stock_url)
    stock_data = json.loads(stock_json)
    sizes = []
    price = 0
    for stock in stock_data['stocks']:
        if stock['productId'] == int(product_id):
            for product_stock in stock['stocks']:
                for product_size in product_sizes:
                    if product_size['sku'] == product_stock['id']:
                        stock_bool = False
                        if product_stock['availability'] == 'in_stock':
                            stock_bool = True
                        size = {
                            "value": product_size['name'],
                            'stock': stock_bool
                        }
                        sizes.append(size)
                        if int(product_size['price'])/100 > price:
                            price = int(product_size['price'])/100
        break
    cont['sizes'] = sizes
    cont['selling_price'] = price
    cont['discount_price'] = price
    cont['original_price'] = price
    product_dict['product'] = cont
    return product_dict


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/links/?brand=massimo'
    # url = 'http://127.0.0.1:8000/api/v1/project/links/?brand=zara'
    links = get_categories_from_db(url)
    length = (len(links))
    print(length)
    ranges = length // 40 + 1
    all_products = []
    get_data(links[0])
    for i in range(ranges):
        range_links = (links[i * 40: (i + 1) * 40])
        if range_links:
            with Pool(20) as p:
                data = (p.map(get_data, range_links))
                all_products.extend(data)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url,
                          data=json.dumps(all_products), headers=headers)
        print(r.status_code)
        all_products = []
        time.sleep(3)


if __name__ == '__main__':
    main()
