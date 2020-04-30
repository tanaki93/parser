import json
from multiprocessing.dummy import Pool
from random import choice

import requests
from bs4 import BeautifulSoup

from koton.constants import PROXIES, USERAGENTS


def get_html(url):
    proxy = {'http': 'http://' + choice(PROXIES)}
    useragent = {'User-Agent': choice(USERAGENTS)}
    r = requests.get(url, headers=useragent, proxies=proxy)
    print(url)
    return r.text


def get_html1(url):
    r = requests.get(url)
    return r.text


def get_categories_from_db(url):
    html = get_html1(url)
    return json.loads(html)


def get_pages_count(html):
    soup = BeautifulSoup(html, 'lxml')
    href = 200
    try:
        href = int(soup.find('div', class_='srch-ttl-cntnr-wrppr').find('div', class_='dscrptn').text.split(' ')[-3])
    except:
        pass
    return href


def get_links(count, link):
    pages = count // 24
    if count % 24 > 0:
        pages += 1
    # links = [link + '?pi=' + str(i) for i in range(1, 2)]
    links = [link + '&pi=' + str(i) for i in range(1, pages + 1)]
    return pages, links


def get_data_links(link):
    html = get_html(link)
    soup = BeautifulSoup(html, 'lxml')
    data = []
    try:
        data = soup.find('div', class_='prdct-cntnr-wrppr').find_all('div', class_='p-card-wrppr')
    except:
        pass
    links = []
    for i in data:
        href = 'https://www.trendyol.com' + (i.find('a', class_='p-card-chldrn-cntnr')['href'].split('?')[0])
        links.append(href)
    return links


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/categories/?brand=JackJones'
    # url = 'http://127.0.0.1:8000/api/v1/project/categories/?brand=Marjin'
    categories = get_categories_from_db(url)
    all_links = []
    for category in categories:
        link = category['link']
        print(link)
        count = get_pages_count(get_html(link))
        pages, links = get_links(count, link)
        context = {
            'category_id': category['id'],
        }
        category_links = []
        with Pool(20) as p:
            data = (p.map(get_data_links, links))
            for i in data:
                category_links.extend(i)
        context['links'] = category_links
        all_links.append(context)
        # break
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url,
                          data=json.dumps(all_links), headers=headers)
        print(r.status_code)
        all_links = []
        # time.sleep(3)

if __name__ == '__main__':
    main()
