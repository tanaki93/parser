#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from random import choice

import requests
from bs4 import BeautifulSoup
from koton.constants import PROXIES, USERAGENTS
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_html(url):
    proxy = {'http': 'http://' + choice(PROXIES)}
    useragent = {'User-Agent': choice(USERAGENTS)}
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_html1(url):
    print(url)
    r = requests.get(url)
    return r.text


def get_html_data(url):
    html = None
    driver = webdriver.Chrome('c://chromedriver.exe')
    driver.get(url)
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'fltrs-wrppr'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    html = driver.page_source
    driver.quit()
    return html


def parse_department_data(department):
    url = department['link']
    html = get_html_data(url)
    if html is not None:
        soup = BeautifulSoup(html, 'lxml')
        data = soup.find('div', id='container').find('div', id='search-app').find('div',
                                                                                  class_='search-app-container') \
            .find('div', class_='srch-rslt-cntnt').find('div', class_='srch-aggrgtn-cntnr').find_all('div',
                                                                                                     class_='fltrs-wrppr')[
            0].find('div', class_='fltrs').find_all('a', class_='fltr-item-wrppr')
        categories = []
        for i in data:
            context = {
                'link': 'https://www.trendyol.com' + i['href'],
                'category': i.find('div', class_='fltr-item-text').text
            }
            categories.append(context)
        return categories
    else:
        return []


def parse_brand_data(brand):
    url = brand['link']
    print(url)
    html = get_html_data(url)
    if html is not None:
        soup = BeautifulSoup(html, 'lxml')
        data = []
        sidebar = soup.find('div', id='container').find('div', id='search-app').find('div',
                                                                                     class_='search-app-container') \
            .find('div', class_='srch-rslt-cntnt').find('div', class_='srch-aggrgtn-cntnr').find_all('div',
                                                                                                     class_='fltrs-wrppr')
        for j in sidebar:
            text = ''
            try:
                text = j.find('div', class_='fltr-cntnr-ttl').text
            except:
                pass
            if text == 'Cinsiyet':
                data = (j.find('div', class_='fltrs').find_all('a', class_='fltr-item-wrppr'))
        departments = []
        for i in data:
            context = {
                'link': 'https://www.trendyol.com' + i['href'],
                'department': i.find('div', class_='fltr-item-text').text
            }
            categories = parse_department_data(context)
            context['categories'] = categories
            departments.append(context)
        return departments
    else:
        return []


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/brands/?brand=Kom'
    # url = 'http://127.0.0.1:8000/api/v1/project/brands/?brand=Bambi'
    html = get_html1(url)
    brands = json.loads(html)
    departments = parse_brand_data(brands)
    # with open('item.json', 'w') as outfile:
    #     json.dump(departments, outfile)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.put(url, data=json.dumps(departments), headers=headers)
    print(r.status_code)


if __name__ == '__main__':
    main()
