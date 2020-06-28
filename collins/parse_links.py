import json
import time
from multiprocessing.dummy import Pool
from pprint import pprint
from random import randint

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from handm.parse_links import get_html1, get_html


def get_pages(category):
    print(category['link'])
    elem = get_html(category['link'])
    soup = BeautifulSoup(elem, 'lxml')
    data = 1
    try:
        data = soup.find('div', id='page').find('div', class_='fullContent top-space') \
            .find('div', class_='container catalog-category') \
            .find('div', class_='productListContainer') \
            .find('div').find('div', class_='productList clearfix') \
            .find('div', class_='module-content product-list clearfix') \
            .find('div', class_='pagerBottomContent').find('div').find_all('a')[-1]['href'].split('pagenumber=')[1]
        data = int(data)
    except:
        pass
    return data


def get_data(category):
    elem = get_html(category)
    links = []
    soup = BeautifulSoup(elem, 'lxml')
    try:
        data = soup.find('div', id='page').find('div', class_='fullContent top-space') \
            .find('div', class_='container catalog-category') \
            .find('div', class_='productListContainer') \
            .find('div').find('div', class_='productList clearfix') \
            .find('div', class_='module-content product-list clearfix') \
            .find('div', class_='row clearfix').find_all('div', class_='col-lg-6 md-6 col-sm-6 col-xs-6')
        for i in data:
            href = 'https://www.colins.com.tr' + \
                   i.find('div').find('div', class_='productWrapper clearfix').find('h4').find('a')['href']
            links.append(href)
    except:
        pass
    return links


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/categories/?brand=COLNS'
    html = get_html1(url)
    categories = json.loads(html)
    all_links = []
    for i in categories:
        pages = get_pages(i)
        links = ['%s%s%s' % (i['link'], '&pagenumber=', num) for num in range(1, pages + 1)]
        context = {
            'category_id': i['id'],
        }
        category_links = []
        with Pool(20) as p:
            data = (p.map(get_data, links))
            for i in data:
                category_links.extend(i)
        context['links'] = category_links
        all_links.append(context)
        print(len(category_links))
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url,
                          data=json.dumps(all_links), headers=headers)
        print(r.status_code)
        all_links = []


if __name__ == '__main__':
    main()
