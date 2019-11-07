#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
from pprint import pprint
from random import choice, randint

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
    html = None
    driver = webdriver.Chrome('C://chromedriver.exe')
    try:
        driver.get(url)
        last_height = driver.execute_script("return document.body.scrollHeight")
        count = 0
        num = 0
        while True:
            num += 1
            count += 4500
            driver.execute_script("window.scrollTo(0, %s);" % count)
            new_height = driver.execute_script("return document.body.scrollHeight")
            time.sleep(0.6)
            if num == 3:
                break
            if new_height == last_height:
                break
            last_height = new_height

        html = driver.page_source
    except:
        pass
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
                'link': 'https://www.trendyol.com'+i['href'],
                'name': i.find('div', class_='fltr-item-text').text
            }
            categories.append(context)
        return categories
    else:
        return []


def parse_brand_data(brand):
    url = brand['link']
    html = get_html_data(url)
    if html is not  None:
        soup = BeautifulSoup(html, 'lxml')
        data = []
        sizes = []
        sizes_trendyol= []
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
            elif text == 'Beden':
                sizes_trendyol = (j.find('div', class_='fltrs').find_all('a', class_='fltr-item-wrppr'))
        for size in sizes_trendyol:
            sizes.append(size.find('div', class_='fltr-item-text').text)
        departments = []
        for i in data:
            context = {
                'link': 'https://www.trendyol.com'+i['href'],
                'name': i.find('div', class_='fltr-item-text').text
            }
            categories = parse_department_data(context)
            context['categories'] = categories
            departments.append(context)
        return departments, sizes
    else:
        return [], []


def main():
    # url = 'http://188.120.242.218:8089/api/v1/project/brands/'
    url = 'http://127.0.0.1:8000/api/v1/project/brands/'
    html = get_html1(url)
    brands = json.loads(html)
    new_brands = []
    for i in brands:
        departments, sizes = parse_brand_data(i)
        data = {
            'name': i['name'],
            'link': i['link'],
            'id': i['id'],
            'departments': departments,
            'sizes': sizes
        }
        new_brands.append(data)
    with open('item.json', 'w') as outfile:
        json.dump(new_brands, outfile)
    # with open('item.json', 'r') as outfile:
    #     new_brands = json.load(outfile)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(url, data=json.dumps(new_brands), headers=headers)
    print(r.status_code)


if __name__ == '__main__':
    main()
