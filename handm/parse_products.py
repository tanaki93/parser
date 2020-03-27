#!/usr/bin/env python
# -*- coding: utf-8
import json
from multiprocessing.dummy import Pool
from pprint import pprint
from random import choice

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


from koton.constants import PROXIES, USERAGENTS


def get_html(url):
    print(url)
    proxy = {'http': 'http://' + choice(PROXIES)}
    useragent = {'User-Agent': choice(USERAGENTS)}
    r = requests.get(url, headers=useragent, proxies=proxy)
    r.raise_for_status()
    return r.text


def get_html1(url):
    r = requests.get(url)
    return r.text


def get_categories_from_db(url):
    html = get_html1(url)
    return json.loads(html)



def get_data(context):
    cont = None
    product = {
        'id': context['id']
    }
    try:
        cont = {}
        url = context['url']
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        scripts = json.loads(soup.find('script', type='application/ld+json').text)
        cont['colour'] = scripts['color']
        cont['description'] = scripts['description']
        cont['name'] = scripts['name']
        cont['product_code'] = scripts['sku']
        cont['selling_price'] = float(scripts['offers'][0]['price'])
        cont['original_price'] = float(scripts['offers'][0]['price'])
        cont['images'] = scripts['image']
        if scripts['offers'][0]['availability'] == 'http://schema.org/InStock':
            stock = True
        else:
            stock = False
        cont['stock'] = stock
        sizes = []
        li = soup.find('main').find('div', class_='product parbase')
        scripts = li.find('script')
        data = (scripts.text.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').strip().split(
            '\'sizes\''))

        data = data[1:]
        for i in data[:-1]:
            text = i[1:]
            index = text.find(']')
            try:
                js = json.loads(text[0:index + 1].replace('\'', '\"'))
                for j in js:
                    if cont['product_code'] + j['size'] == j['sizeCode']:
                        size = {'value': j['name'], 'stock': False, 'code': j['sizeCode']}
                        sizes.append(size)
            except:
                pass
        service = 'https://www2.hm.com/hmwebservices/service/product/tr/availability/%s.json' % cont['product_code'][
                                                                                                0:-3]
        h = get_html(service)
        n = BeautifulSoup(h, 'lxml')
        size_data = (json.loads(n.text))
        new_sizes = []
        for i in size_data['availability']:
            for j in sizes:
                if j['code'] == i:
                    new_sizes.append(i)
                    break
        available = []
        count = len(new_sizes)
        for i in sizes:
            flag = 0
            for j in new_sizes:
                if i['code'] == j:
                    continue
                else:
                    flag += 1
            if flag != count and i not in available:
                available.append({'value': i['value'], 'stock': True, 'code': i['code']})
            else:
                available.append({'value': i['value'], 'stock': False, 'code': i['code']})
        cont['sizes'] = available
    except:
        pass
    product['product'] = cont
    return product


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/links/?brand=HANDM'
    # context = {
    #     'id': 1,
    #     'url':'https://www2.hm.com/tr_tr/productpage.0738736001.html'
    # }
    # product = get_data(context)
    # pprint(product)
    # url = 'http://127.0.0.1:8000/api/v1/project/links/?brand=handm'
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
