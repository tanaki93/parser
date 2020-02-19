import json
from pprint import pprint
from random import uniform
from time import sleep

import requests
from bs4 import BeautifulSoup

from koton.parse_category import get_html, get_html1


def get_data(context):
    html = get_html('https://www.colins.com.tr/urun/893-julia-normal-kesim-orta-bel-kisa-paca-mavi-jean-pantolon-16434')
    data = {}
    soup = BeautifulSoup(html, 'lxml')
    base = soup.find('div', id='page').find('div', class_='fullContent top-space').find('div').find('div').find(
        'div').find('div', class_='row product-details-page').find('div').find('form')
    images_soup = base.find('div', class_='productDetailLeftPanel col-lg-6 col-sm-6').find('div').find('div').find(
        'div', class_='module-frameproduct-picture-wrapper').find('div').find_all('a')
    description = ''
    try:
        tr = (soup.find('div', id='page').find('div', class_='fullContent top-space').find('div').find('div').find(
            'div').find('div', class_='product-details-mobile row').find('div').find('div',
                                                                                     class_='PDTABSCONTENT clearfix tab-content').find(
            'div', class_='tab-pane active').find('table').find('tbody').find_all('tr')[1])
        description = tr.find('td').text.strip()
    except:
        pass

    images = []
    for i in images_soup:
        images.append(i['data-image'])
    right = base.find('div', class_='productDetailRightPanel')
    name_soup = right.find('h1')
    name = name_soup.text.strip()
    others = right.find('div', class_='product-collateral').find('div').find('div', class_='variant-wrapper').find(
        'div')
    color = others['data-variant-name'].lower().capitalize()
    price = others.find('div', class_='productPriceContent clearfix').find('span').text.strip().split(' ')[
        0].replace(',', '.')
    variants = others.find('div', class_='product-options').find('div').find_all('div')
    sizes = []
    for i in variants:
        classes = i['class']
        size = {
            'value': i.find('label').text.strip()
        }
        if len(classes) == 2:
            size['stock'] = False
        else:
            size['stock'] = True
        sizes.append(size)
    print(sizes)
    return []


def main():
    get_data('')


if __name__ == '__main__':
    main()
