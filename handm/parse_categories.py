import json

import requests
from bs4 import BeautifulSoup

from koton.parse_category import get_html1, get_html


def parse_brand_data(brand):
    data = [{'name': 'Kadın', 'link': 'https://www2.hm.com/tr_tr/kadin.html'},
            {'name': 'Erkek', 'link': 'https://www2.hm.com/tr_tr/erkek.html'},
            {'name': 'Divided', 'link': 'https://www2.hm.com/tr_tr/divided.html'},
            {'name': 'Çocuk', 'link': 'https://www2.hm.com/tr_tr/cocuk.html'},
            ]
    l = []
    for i in data:
        context = {
            'department': i['name'],
            'link': i['link']
        }
        html = get_html(context['link'])
        soup = BeautifulSoup(html, 'lxml')
        menu = soup.find('div', class_='sidebar-plus-content').find('aside', class_='page-sidebar').find('nav',
                                                                                                         class_='secondary-nav') \
            .find('ul', id='menu-links').find_all('li', class_='list-group')
        all_categories = []
        for i in menu:
            menu_item = None
            try:
                menu_item = i.find('strong', class_='list-group-title is-opened')
            except:
                pass
            if menu_item is not None:
                ul = i.find('ul', class_='menu').find_all('li')
                for j in ul:
                    category = {}
                    a = j.find('a')
                    if a['href'] != '/tr_tr/kadin/urune-gore-satin-al/view-all.html' \
                            or a['href'] != '/tr_tr/erkek/urune-gore-satin-al/view-all.html'\
                            or a['href'] != '/tr_tr/cocuk/urune-gore-satin-al/view-all.html':
                        category['link'] = 'https://www2.hm.com'+a['href']
                        category['name'] = a.text.strip()
                        all_categories.append(category)
        context['categories'] = all_categories
        l.append(context)
    return l


def main():
    url = 'http://188.120.242.218:8089/api/v1/project/brands/handm/'
    # url = 'http://127.0.0.1:8000/api/v1/project/brands/handm/'
    html = get_html1(url)
    zara = json.loads(html)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.status_code)


if __name__ == '__main__':
    main()
