import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from koton.parse_category import get_html1, get_html


def parse_brand_data(brand):
    data = [{'name': 'Kadın', 'link': 'https://www.colins.com.tr/c/kadin-giyim-57'},
            {'name': 'Erkek', 'link': 'https://www.colins.com.tr/c/erkek-giyim-2'},
            {'name': 'Aksesuar', 'link': 'https://www.colins.com.tr/c/aksesuar-465'}, ]
    l = []
    for i in data:
        context = {
            'department': i['name'],
            'link': i['link']
        }
        html = get_html(context['link'])
        soup = BeautifulSoup(html, 'lxml')
        menu = soup.find('div', id='page').find('div', class_='fullContent top-space').find('div',
                                                                                            class_='container catalog-category') \
            .find('div', class_='productFilterContent').find('div',
                                                             class_='panel-heading clearfix group-container-Kategori') \
            .find('div').find('div').find('ul').find_all('li')
        pprint(menu)
        categories = []
        for i in menu:
            category = {
                'category': i.find('a').text.strip(),
                'link': i.find('a')['href'],
            }
            categories.append(category)
        context['categories'] = categories
        l.append(context)
    return l


def main():
    url = 'http://188.120.242.218:8089/api/v1/project/brands/?brand=Collins'
    # url = 'http://127.0.0.1:8000/api/v1/project/brands/?brand=Collins'
    html = get_html1(url)
    collins = json.loads(html)
    data = parse_brand_data(collins)
    pprint(data)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r.status_code)


if __name__ == '__main__':
    main()
