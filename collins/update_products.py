#!/usr/bin/env python
# -*- coding: utf-8
import json
from datetime import datetime
from multiprocessing.dummy import Pool
from random import choice

import requests
from bs4 import BeautifulSoup

from .constants import PROXIES, USERAGENTS


def get_html(url):
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
    product = None
    cont = {
        'id': context['id']
    }
    html = get_html(context['url'])
    product = {}
    soup = BeautifulSoup(html, 'lxml')
    try:
        base = soup.find('div', id='page').find('div', class_='fullContent top-space').find('div').find('div').find(
            'div').find('div', class_='row product-details-page').find('div').find('form')
        images_soup = base.find('div', class_='productDetailLeftPanel col-lg-6 col-sm-6').find('div').find('div').find(
            'div', class_='module-frameproduct-picture-wrapper').find('div').find_all('a')

        description = ''
        try:
            tr = (soup.find('div', id='page').find('div', class_='fullContent top-space').find('div').find('div').find(
                'div').find('div', class_='product-details-mobile row').find('div').find('div',
                                                                                         class_='PDTABSCONTENT clearfix tab-content').find(
                'div', class_='tab-pane active').find('table').find('tbody').find_all('tr')[1])
            description = tr.find('td').text.strip()
        except:
            pass

        images = []
        for i in images_soup:
            images.append(i['data-image'])
        right = base.find('div', class_='productDetailRightPanel')
        name_soup = right.find('h1')
        name = name_soup.text.strip()
        others = right.find('div', class_='product-collateral').find('div').find('div', class_='variant-wrapper').find(
            'div')
        product['stock'] = False
        color = others['data-variant-name'].lower().capitalize()
        price = others.find('div', class_='productPriceContent clearfix').find('span').text.strip().split(' ')[
            0].replace(',', '.')
        variants = others.find('div', class_='product-options').find('div').find_all('div')
        sizes = []
        for i in variants:
            classes = i['class']
            size = {
                'value': i.find('label').text.strip()
            }
            if len(classes) == 2:
                size['stock'] = False
            else:
                size['stock'] = True
                product['stock'] = True
            sizes.append(size)
        product['description'] = description
        product['name'] = name
        product['colour'] = color
        product['price'] = price
        product['sizes'] = sizes
        product['images'] = images
        cont['product'] = product
    except:
        cont['product'] = None
        print(context['url'])
        pass
    return cont


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/update/links/?brand=collins'
    # url = 'http://127.0.0.1:8000/api/v1/project/update/links/?brand=collins'
    links = get_categories_from_db(url)
    length = (len(links))
    print(length, datetime.now())
    ranges = length // 40 + 1
    all_products = []
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


if __name__ == '__main__':
    main()
