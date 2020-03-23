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
        product = {}

        main_data = soup.find('div', id='page-container').find('section', id='main').find('section', id='product')
        script = main_data.find('script').contents[0]
        script = json.loads(script, strict=False)
        images_data = main_data.find('div', class_='product-images-section _product-images-section') \
            .find('div', class_='big-image-container _big-image-container').find('div', id='main-images').find_all(
            'div',
            class_='media-wrap')
        images = []
        form = main_data.find('form')
        sizes = []
        colour = main_data.find('div', class_='info-section').find('div',
                                                                   class_='product-info-wrapper _product-info').find(
            'p').find('span', class_='_colorName').text
        for i in (form.find('div', class_='size-select _size-select').find_all('label', class_='product-size')):
            input = i.find('div', class_='aria-size-input').find('input')
            size = {
                'value': input['value']
            }
            disabled = None
            try:
                disabled = input['disabled']
            except:
                pass
            if disabled is None:
                size['stock'] = True
            else:
                size['stock'] = False
            sizes.append(size)
        info = script[0]
        for i in images_data:
            images.append(i.find('a', class_='_seoImg main-image')['href'])
        product['images'] = images
        product['selling_price'] = float(info['offers']['price'])
        product['name'] = info['name']
        product['description'] = info['description']
        product['sizes'] = sizes
        product['colour'] = colour.lower().capitalize()
        cont = {
            'id': context['id'],
            'product': product
        }
    except:
        pass
    return cont


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/links/?brand=zara'
    # url = 'http://127.0.0.1:8000/api/v1/project/links/?brand=zara'
    links = get_categories_from_db(url)
    length = (len(links))
    print(length)
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
