import json
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
    project_url = 'https://www.massimodutti.com/itxrest/2/catalog/store/34009471/30359503/category/%s/product?languageId=-43&appId=2'
    link = category['link']
    category_id = link.split('-c')[-1].split('.html')[0]
    url = (project_url % category_id)
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pprint(soup.text)
    json_data = json.loads(soup.text)
    links = link.split('-c')[0:-1]
    n_category = {
        'category_id': category['id']
    }
    n_links = []
    text = ''
    for i in links:
        text += i
    for category_obj in json_data['products']:
        product_urls = category_obj['productUrl']
        if len(category_obj['bundleProductSummaries'])>0:
            id = category_obj['bundleProductSummaries'][0]['id']
            detail = category_obj['bundleProductSummaries'][0]['detail']
        else:
            id = category_obj['id']
            detail = category_obj['detail']
        product_url = ''
        for i in product_urls.split('-')[0:-1]:
            product_url += (i + '-')
        product_url = product_url[0:-1]
        for i in detail['colors']:
            new_text = text + '/' + product_url + '-c' + category_id + 'p' + str(id) + '.html' + '?colorId=' + i[
                'id'] + '&category_id=' + category_id
            n_links.append(new_text)
    n_category['links'] = n_links
    pprint(n_category)
    return n_category


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/categories/?brand=MDT'
    html = get_html1(url)
    soup = BeautifulSoup(html, 'lxml')
    json_data = json.loads(soup.text)
    all_links = []
    for i in json_data:
        all_links.append(get_data_links(i))
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url,
                          data=json.dumps(all_links), headers=headers)
        print(r.status_code)

        all_links = []


if __name__ == '__main__':
    main()
