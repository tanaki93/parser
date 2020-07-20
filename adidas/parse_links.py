import sys
import json
from pprint import pprint

import requests
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage
from bs4 import BeautifulSoup
from selenium import webdriver


class Client(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def on_page_load(self):
        self.app.quit()


def get_html1(url):
    r = requests.get(url)
    return r.text


def get_categories_from_db(url):
    html = get_html1(url)
    return json.loads(html)


def get_links(data):
    links = []
    for i in (data.find('ul', class_='emosInfinite ems-inline').find_all('li', class_='ems-prd  filter')):
        links.append(
            i.find('div').find('div', class_='ems-prd-mask').find('div', class_='ems-prd-image').find('a')['href'])
    return links


def get_data(url):
    print(url)
    source = get_html_data('https://'+url)
    soup = BeautifulSoup(source, 'lxml')
    data = soup.find('form', id='aspnetForm').find('div', class_='wrapper').find('div', class_='sayfaDisDiv').find(
        'div').find('div', class_='site-wrapper')
    right = data.find('main').find('div', class_='filter-selected').find('div').find('div',
                                                                                     class_='ems-container-section').find(
        'div', class_='ems-col ems-col-right').find('div').find('div').find('div', id='ajxUrunList').find('div')
    return get_links(right)


def get_html_data(url):
    html = None
    driver = webdriver.Chrome('c://chromedriver.exe')
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html


def get_data_links(category):
    url = category['link']
    source = get_html_data('https://'+url)
    soup = BeautifulSoup(source, 'lxml')
    try:
        data = soup.find('form', id='aspnetForm').find('div', class_='wrapper').find('div', class_='sayfaDisDiv').find(
            'div').find('div', class_='site-wrapper')
        right = data.find('main').find('div', class_='filter-selected').find('div').find('div',
                                                                                         class_='ems-container-section').find(
            'div', class_='ems-col ems-col-right').find('div').find('div').find('div', id='ajxUrunList').find('div')
    except:
        pass
    right = None
    count = None
    try:
        count = int(
            right.find('div', class_='ems-prd-list-prop').find('div', class_='ems-prd-list-prop-inner').find('div',
                                                                                                             class_='ems-prd-list-count').find_all(
                'span')[-1].text.split(' ')[0])
    except:
        pass
    links = []
    if count is not None:
        page = count // 26 + 1
        print(page, count)
        links.extend(get_links(right))

        if page > 1:
            for p in range(2, page + 1):
                links.extend(get_data(str(url + '&page=' + str(p))))

    cont = {
        'category_id': category['id'],
        'links': links
    }
    return cont


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/categories/?brand=ADIDAS'
    categories = get_categories_from_db(url)
    for i in categories:
        all_links = [get_data_links(i)]
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url,
                          data=json.dumps(all_links), headers=headers)
        print(r.status_code)


if __name__ == '__main__':
    main()
