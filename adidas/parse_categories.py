import json
import sys
from pprint import pprint

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
import requests
from bs4 import BeautifulSoup

from koton.parse_category import get_html1, get_html

DEPARTMENTS = [
    {
        'name': 'ERKEK',
        'code': '?opf=p6051585'
    },
    {
        'name': 'KADIN',
        'code': '?opf=p6051586'
    },
    {
        'name': 'COCUK',
        'code': '?opf=p6051584'
    },
]


class Client(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def on_page_load(self):
        self.app.quit()



def parse_brand_data(brand):
    url = brand['link']
    html = Client(url)
    source = html.mainFrame().toHtml()
    brand = url.split('/')[3]
    print(brand)
    soup = BeautifulSoup(source, 'lxml')
    data = soup.find('form', id='aspnetForm').find('div', class_='wrapper').find('div', class_='sayfaDisDiv').find(
        'div').find('div', class_='site-wrapper')
    main = data.find('main').find('div', class_='filter-selected').find('div').find('div',
                                                                                    class_='ems-container-section').find(
        'div', class_='ems-col ems-col-left') \
        .find('div', class_='ems-col-inner').find('div', class_='ems-cell ems-cell-1 sortable').find('div').find('div',
                                                                                                                 class_='kutuBodyDefault kutuBodyKategori') \
        .find('div').find('ul')
    parents = main.find_all('li', class_='s1')
    departments = []
    for dep in DEPARTMENTS:
        department = {
            'department': dep['name']
        }
        categories = []
        for parent in parents:
            parent_text = parent.find('a').text
            if parent_text == 'ÇOCUK' or parent_text == 'GÜNLÜK' or parent_text == 'TAKIM SPORLARI' or parent_text == 'FIRSAT KÖŞESİ':
                continue
            else:
                categories_data = parent.find('ul').find_all('li', class_='s2')
                for category in categories_data:
                    a = category.find('a')
                    cat = {
                        'category': a.text+' ('+parent_text+')',
                        'link': 'www.korayspor.com'+a['href']+dep['code']
                    }
                    categories.append(cat)
        department['categories'] = categories
        departments.append(department)
    return departments


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/brands/?brand=Adidas'
    # url = 'http://127.0.0.1:8000/api/v1/project/brands/zara/'
    html = get_html1(url)
    js = json.loads(html)
    data = parse_brand_data(js)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r.status_code)


if __name__ == '__main__':
    main()
