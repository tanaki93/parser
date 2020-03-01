#!/usr/bin/env python
# -*- coding: utf-8
import json
from multiprocessing.dummy import Pool
from random import choice

import requests
from bs4 import BeautifulSoup

from koton.constants import PROXIES, USERAGENTS


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


def get_data(context):
    cont = {}
    try:
        html = get_html(context['url'])
        soup = BeautifulSoup(html, 'lxml')
        href = \
            soup.find('div', id='container').select('script')[2].text.split(
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
    url = 'https://magicbox.izishop.kg/api/v1/project/links/?brand=slazenger'
    # url = 'http://127.0.0.1:8000/api/v1/project/links/?brand=koton'
    links = get_categories_from_db(url)
    length = (len(links))
    print(length)
    ranges = length // 40 + 1
    all_products = []
    for i in range(ranges):
        range_links = (links[i * 40: (i + 1) * 40])
        if range_links:
            with Pool(40) as p:
                data = (p.map(get_data, range_links))
                all_products.extend(data)

        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url,
                          data=json.dumps(all_products), headers=headers)
        print(r.status_code)
        all_products = []


if __name__ == '__main__':
    main()
