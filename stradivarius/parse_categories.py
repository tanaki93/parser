import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from koton.parse_category import get_html1, get_html


def parse_brand_data(brand):
    url = brand['link']
    print(url)


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/brands/?brand=stradivarius'
    # url = 'http://127.0.0.1:8000/api/v1/project/brands/?brand=stradivarius'
    request_url = 'https://www.stradivarius.com/itxrest/2/catalog/store/54009571/50331081/category?languageId=-43&typeCatalog=1&appId=2'
    html = get_html(request_url)
    stradivarius = json.loads(html)
    categories = stradivarius['categories'][0]['subcategories']
    new_categories = [categories[1], categories[3]]
    departments = []
    department = {
        'department': 'Kadin',
        'link': 'https://www.stradivarius.com/tr/',
    }
    sub_categories = []
    for i in new_categories:
        parent = i['subcategories'][0]

        for category in parent['subcategories'][1:]:
            if len(category['subcategories']) == 0:
                print(category['name'])
                n_category = {
                    'category': category['name'],
                    'link': 'https://www.stradivarius.com/tr/yeni-koleksiyon/%s/ürüne-göre-alışveriş/%s-c%s.html' % (
                        str(i['name']).lower(), str(category['name']).replace(' ', '-').lower(), category['id'])
                }
                sub_categories.append(n_category)
            elif len(category['subcategories']) > 0:
                for sub in category['subcategories'][1:]:
                    n_category = {
                        'category': '%s (%s)' % (category['name'], sub['name']),
                        'link': 'https://www.stradivarius.com/tr/yeni-koleksi̇yon/%s/ürüne-göre-alışveriş/%s/%s-c%s.html' % (
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


if __name__ == '__main__':
    main()
