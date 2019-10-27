#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from pprint import pprint
from random import choice

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from constants import PROXIES, USERAGENTS


def get_html(url):
    proxy = {'http': 'http://' + choice(PROXIES)}
    useragent = {'User-Agent': choice(USERAGENTS)}
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_html1(url):
    r = requests.get(url)
    return r.text


def get_html_data(url):
    browser = webdriver.Chrome(executable_path=r'C:\chromedriver.exe')
    browser.get(url)
    html = browser.page_source
    return html


def parse_department_data(department):
    url = 'https://www.trendyol.com' + department['link']
    html = get_html_data(url)
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find('div', id='container').find('div', id='search-app').find('div',
                                                                              class_='search-app-container') \
        .find('div', class_='srch-rslt-cntnt').find('div', class_='srch-aggrgtn-cntnr').find_all('div',
                                                                                                 class_='fltrs-wrppr')[
        0].find('div', class_='fltrs').find_all('a', class_='fltr-item-wrppr')
    print(data)
    categories = []
    for i in data:
        context = {
            'link': i['href'],
            'name': i.find('div', class_='fltr-item-text').text
        }
        categories.append(context)
    return categories


def parse_brand_data(brand):
    url = 'https://www.trendyol.com/' + brand['name']
    html = get_html_data(url)
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find('div', id='container').find('div', id='search-app').find('div',
                                                                              class_='search-app-container') \
        .find('div', class_='srch-rslt-cntnt').find('div', class_='srch-aggrgtn-cntnr').find_all('div',
                                                                                                 class_='fltrs-wrppr')[
        1].find('div', class_='fltrs').find_all('a', class_='fltr-item-wrppr')
    departments = []
    for i in data:
        context = {
            'link': i['href'],
            'name': i.find('div', class_='fltr-item-text').text
        }
        categories = parse_department_data(context)
        context['categories'] = categories
        departments.append(context)
    pprint(departments)


def main():
    url = 'http://127.0.0.1:8000/api/v1/project/brands/'
    html = get_html1(url)
    brands = json.loads(html)
    print(brands)
    for i in brands:
        parse_brand_data(i)


if __name__ == '__main__':
    main()
