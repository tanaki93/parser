import json
import time
from multiprocessing.dummy import Pool
from pprint import pprint
from random import choice

import requests
from bs4 import BeautifulSoup

from koton.constants import PROXIES, USERAGENTS


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


def get_data_links(category):
    project_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/25009521/20309411/category/%s/product?languageId=-43&showProducts=false&appId=1'
    link = category['link']
    category_id = link.split('-c')[-1].split('.html')[0]
    url = (project_url % category_id)
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    json_data = json.loads(soup.text)
    links = link.split('-c')[0:-1]
    n_category = {
        'category_id': category['id']
    }
    ids = []
    text = ''
    for i in links:
        text += i
    for id in json_data['productIds']:
        ids.append(id)
    pprint(len(ids))
    new_url = 'https://www.pullandbear.com/itxrest/3/catalog/store/25009521/20309411/productsArray?productIds=%s&languageId=-43&categoryId=1030061504&appId=1'
    url_text = str(ids[0])
    for i in range(1, len(ids)):
        url_text += '%2C' + str(ids[i])
    html = get_html(new_url % url_text)
    soup = BeautifulSoup(html, 'lxml')
    json_data = json.loads(soup.text)
    n_links = []
    for category_obj in json_data['products']:
        colorId = category_obj['mainColorid']
        product_urls = category_obj['productUrl']
        product_url = ''
        for i in product_urls.split('-')[0:-1]:
            product_url += (i + '-')
        product_url = product_url[0:-1]
        new_text = text + '/' + product_url + '-c' + category_id + 'p' + str(
            category_obj['id']) + '.html' + '?cS=' + str(colorId)
        n_links.append(new_text)
    n_category['links'] = n_links
    pprint(n_category)
    return n_category


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/categories/?brand=PLLBR'
    html = get_html1(url)
    soup = BeautifulSoup(html, 'lxml')
    json_data = json.loads(soup.text)
    array_links = []
    for i in json_data:
        array_links.append(get_data_links(i))
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url,
                          data=json.dumps(array_links), headers=headers)
        print(r.status_code)
        array_links = []
        time.sleep(2)
        # break


if __name__ == '__main__':
    main()
