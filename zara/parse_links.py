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
    link = category['link']
    print(link)
    all_links = []
    new = {
        'category_id': category['id']
    }
    category_links = []
    html = get_html1(link)
    soup = BeautifulSoup(html, 'lxml')
    data = None
    try:
        data = soup.find('div', id='page-container').find('section', id='main').find('div').find('section',
                                                                                                 id='products').find(
            'div', class_='_groups-wrap') \
            .find('ul', class_='product-list _productList').find_all('li', class_='product')
    except:
        pass
    if data is not None:
        for i in data:
            href = i.find('a', class_='item')
            if href is not None:
                print(href['href'])
                category_links.append(href['href'])
        new['links'] = category_links
        all_links.append(new)
    return all_links


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/categories/?brand=Zara'
    # url = 'http://127.0.0.1:8000/api/v1/project/categories/?brand=zara'
    categories = get_categories_from_db(url)
    all_links = []
    with Pool(20) as p:
        data = (p.map(get_data_links, categories))
        for i in data:
            all_links.extend(i)
        pprint(len(all_links))
        with open('item.json', 'w') as outfile:
            json.dump(all_links, outfile)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url,
                          data=json.dumps(all_links), headers=headers)
        print(r.status_code)


if __name__ == '__main__':
    main()
