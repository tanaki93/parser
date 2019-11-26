#!/usr/bin/env python
# -*- coding: utf-8
import json
import time
from multiprocessing import Pool
from pprint import pprint
from random import choice
import random

import requests
from bs4 import BeautifulSoup
from googletrans import Translator

from constants import PROXIES, USERAGENTS


def get_html(url):
    print(url)
    proxy = {'http': 'http://' + choice(PROXIES)}
    useragent = {'User-Agent': choice(USERAGENTS)}
    # print(proxy)
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_html1(url):
    r = requests.get(url)
    return r.text


def get_categories_from_db(url):
    html = get_html1(url)
    return json.loads(html)


def translate_text(text):
    translator = Translator(service_urls=['translate.google.com.tr'])
    data = u'' + translator.translate(text, dest='ru').text
    return data


def get_data(context):
    cont = {}
    try:
        html = get_html(context['url'])
        soup = BeautifulSoup(html, 'lxml')
        href = \
            soup.find('div', id='container').select('script')[1].text.split(
                'window.__PRODUCT_DETAIL_APP_INITIAL_STATE__ = ')[
                -1].strip()
        data = (json.loads(href[:-1]))
        cont = {
            'id': context['id'],
            'product': data['product'],
        }
    except:
        pass
    return cont


def main():
    # url = 'http://188.120.242.218:8089/api/v1/project/links/trendyol/'
    url = 'http://127.0.0.1:8000/api/v1/project/links/trendyol/'
    links = get_categories_from_db(url)
    length = (len(links))
    ranges = length // 20 + 1
    all_products = []
    for i in range(ranges):
        range_links = (links[i * 20: (i + 1) * 20])
        if range_links:
            with Pool(20) as p:
                data = (p.map(get_data, range_links))
                all_products.extend(data)

        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url,
                          data=json.dumps(all_products), headers=headers)
        print(r.status_code)
        # break
        all_products = []
        break
    # with open('datas.json', 'w', encoding='utf-8') as outfile:
    #     json.dump(all_products, outfile)


if __name__ == '__main__':
    main()
