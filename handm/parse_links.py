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
    link = category['link'] + '?offset=0&page-size=9999'
    print(link)
    all_links = []
    new = {
        'category_id': category['id']
    }
    html = get_html(link)
    soup = BeautifulSoup(html, 'lxml')
    try:
        menu = soup.find('div', class_='sidebar-plus-content').find('div', class_='page-content').find('div',
                                                                                                       class_='main parsys').find_all(
            'div', class_='section')[-1]
        products = (menu.find('ul', class_='products-listing small').find_all('li', class_='product-item'))
        for i in products:
            product = i.find('article').find('div', class_='item-details').find('ul').find_all('li')
            for j in product:
                link = 'https://www2.hm.com' + j.find('a')['href']
                url = link.split('/')
                if url[3] == 'm':
                    link = 'https://www2.hm.com/tr_tr/%s' % (url[-1])
                all_links.append(link)
    except:
        pass
    new['links'] = all_links
    return new


def main():
    # url = 'https://magicbox.izishop.kg/api/v1/project/categories/?brand=handm'
    url = 'http://127.0.0.1:8000/api/v1/project/categories/?brand=handm'
    categories = get_categories_from_db(url)
    all_links = []
    count = 0
    for category in categories[1:]:
        count += 1
        print(count)
        l = [category]
        with Pool(20) as p:
            data = (p.map(get_data_links, l))
            for i in data:
                all_links.append(i)
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            print(len(all_links))
            r = requests.post(url,
                              data=json.dumps(all_links), headers=headers)
            print(r.status_code)
            all_links = []


if __name__ == '__main__':
    main()
