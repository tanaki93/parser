import json

import requests
from bs4 import BeautifulSoup

from koton.parse_category import get_html1, get_html


def parse_brand_data(brand):
    url = brand['link']
    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')
    data = soup.find('div', id='nav-menu-group').find('nav', id='menu').find('ul', class_='category-menu') \
        .find_all('li', class_='_category-link-wrapper menu-item menu-item--level-1')
    data = data[1:5]
    l = []
    for i in data:
        context = {
            'department': i['data-name'],
            'link': i.find('a', class_='_category-link menu-item__category-link')['href']
        }
        html = get_html(context['link'])
        soup = BeautifulSoup(html, 'lxml')
        departments = soup.find('div', id='nav-menu-group').find('nav', id='menu').find('ul', class_='category-menu') \
            .find('li',
                  class_='_category-link-wrapper menu-item menu-item--level-1 menu-item--current menu-item--selected')
        ul = departments.find('ul',
                              class_='_subcategories subcategory-menu subcategory-menu--level-1 subcategory-menu--current')
        classes = (ul.find_all('li', class_='_category-link-wrapper menu-item menu-item--level-2'))
        categories = []
        for classi in classes:
            name = classi['data-name']
            cats = classi.find('ul', class_='_subcategories subcategory-menu subcategory-menu--level-2') \
                .find_all('li', class_='_category-link-wrapper menu-item menu-item--level-3 menu-item--is-leaf')
            cats = cats[1:]
            for category in cats:
                category_data = {
                    'category': '%s (%s)' % (category['data-name'], name)
                }
                try:
                    link = category.find('a', class_='_category-link menu-item__category-link')['href']
                except:
                    link = category.find('a', class_='_category-link menu-item__category-link')['data-href']
                category_data['link'] = link
                categories.append(category_data)
        leafs = (ul.find_all('li', class_='_category-link-wrapper menu-item menu-item--level-2 menu-item--is-leaf'))
        for leaf in leafs:
            class_data = {
                'category': leaf['data-name']
            }
            try:
                link = leaf.find('a', class_='_category-link menu-item__category-link')['href']
            except:
                link = leaf.find('a', class_='_category-link menu-item__category-link')['data-href']
            class_data['link'] = link
            categories.append(class_data)
        context['categories'] = categories
        l.append(context)
    return l


def main():
    url = 'http://188.120.242.218:8089/api/v1/project/brands/zara/'
    # url = 'http://127.0.0.1:8000/api/v1/project/brands/zara/'
    html = get_html1(url)
    zara = json.loads(html)
    data = parse_brand_data(zara)
    with open('categories.json', 'w') as outfile:
        json.dump(data, outfile)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.status_code)


if __name__ == '__main__':
    main()
