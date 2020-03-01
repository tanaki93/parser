import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from koton.parse_category import get_html1, get_html


def parse_brand_data(brand):
    url = brand['link']
    print(url)


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/brands/?brand=bershka'
    # url = 'http://127.0.0.1:8000/api/v1/project/brands/zara/'
    request_url = 'https://www.bershka.com/itxrest/2/catalog/store/44109521/40259537/category?languageId=-43&typeCatalog=1&appId=2'
    html = get_html(request_url)
    massimo = json.loads(html)
    categories = [massimo['categories'][0], massimo['categories'][3]]
    departments = []
    for i in categories:
        department = {
            'department': i['name'],
            'link': 'https://www.bershka.com/tr/',
        }
        collection = None
        for j in i['subcategories']:
            if j['name'] == 'KOLEKSİYON':
                collection = j
                break
        sub_categories = []
        for category in collection['subcategories']:
            if len(category['subcategories']) == 0 and category['viewCategoryId'] > 0:
                n_category = {
                    'category': category['name'],
                    'link': 'https://www.bershka.com/tr/%s/koleksi̇yon/%s-c%s.html' % (
                        str(i['name']).lower(), str(category['name']).replace(' ', '-').lower(), category['id'])
                }
                sub_categories.append(n_category)
            elif len(category['subcategories']) > 0:
                for sub in category['subcategories'][1:]:
                    n_category = {
                        'category': '%s (%s)' % (category['name'], sub['name']),
                        'link': 'https://www.bershka.com/tr/%s/koleksi̇yon/%s/%s-c%s.html' % (
                            str(i['name']).lower(), str(category['name']).replace(' ', '-').lower(),
                            str(sub['name']).replace(' ', '-').lower(), sub['id'])
                    }
                    sub_categories.append(n_category)
        department['categories'] = sub_categories
        departments.append(department)
    pprint(departments)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.put(url, data=json.dumps(departments), headers=headers)
    print(r.status_code)
    departments = []


if __name__ == '__main__':
    main()
