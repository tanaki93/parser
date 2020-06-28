#!/usr/bin/env python
# -*- coding: utf-8
import json
import random
import time
from datetime import datetime
from multiprocessing.dummy import Pool
from pprint import pprint
from random import choice

import requests
from bs4 import BeautifulSoup

PROXIES = [
    "103.253.147.9:8080",
    "101.78.219.178:8080",
    "1.55.240.156:53281",
    "103.42.85.46:53281",
    "103.43.202.18:62225",
    "103.76.170.26:65103",
    "101.255.56.134:53281",
    "103.12.161.1:65103",
    "103.67.198.228:53281",
    "103.244.36.28:65205",
    "103.8.194.2:53281",
    "103.218.100.194:65103",
    "1.234.75.14:80",
    "109.121.161.192:53281",
    "103.9.134.254:65301",
    "109.167.200.84:65309",
    "109.161.48.228:53281",
    "109.236.113.1:8080",
    "109.122.87.33:53281",
    "109.197.190.34:53281",
    "109.121.163.56:53281",
    "104.131.191.119:3128",
    "109.72.232.135:53281",
    "109.236.113.3:8080",
    "111.56.5.41:80",
    "103.78.22.47:53281",
    "103.8.194.6:53281",
    "114.134.186.25:65103",
    "114.159.167.211:8080",
    "116.212.140.13:65205",
    "117.135.198.2:80",
    "117.135.198.9:80",
    "117.102.88.130:65103",
    "117.52.91.248:80",
    "117.6.161.118:53281",
    "103.37.95.110:8080",
    "119.15.171.166:65205",
    "119.15.171.81:65309",
    "122.192.66.50:808",
    "118.70.109.221:53281",
    "122.228.179.178:80",
    "128.199.75.57:443",
    "128.199.75.57:8080",
    "128.199.75.94:3128",
    "128.199.75.94:8080",
    "128.199.75.94:80",
    "128.199.75.94:443",
    "128.199.75.57:3128",
    "137.74.254.198:3128",
    "13.73.1.69:80",
    "128.199.66.186:80",
    "128.199.66.186:443",
    "128.199.66.186:3128",
    "13.126.69.46:80",
    "131.117.214.38:65103",
    "128.199.75.123:80",
    "128.199.75.123:443",
    "139.59.117.11:3128",
    "139.59.125.112:3128",
    "139.59.125.112:443",
    "139.59.125.112:80",
    "137.59.2.9:65205",
    "139.59.125.112:8080",
    "139.59.125.12:443",
    "139.59.125.12:80",
    "139.59.125.53:3128",
    "139.59.125.53:80",
    "139.59.125.53:8080",
    "139.255.97.10:65103",
    "139.59.125.77:3128",
    "139.59.125.77:443",
    "139.59.125.77:80",
    "139.59.125.77:8080",
    "130.117.173.194:65309",
    "145.255.28.218:53281",
    "128.199.138.78:8080",
    "128.199.138.78:80",
    "128.199.138.78:443",
    "139.59.243.186:8080",
    "139.59.243.186:80",
    "128.199.190.243:3128",
    "128.199.190.243:80",
    "128.199.190.243:8080",
    "139.196.36.156:3128",
    "128.199.191.123:80",
    "128.199.191.123:443",
    "149.56.36.54:80",
    "139.59.168.32:8118",
    "154.66.122.130:53281",
    "154.72.74.82:53281",
    "151.237.210.199:53281",
    "159.255.162.222:53281",
    "129.205.210.90:65205",
    "165.84.167.54:8080",
    "164.160.142.60:53281",
    "163.53.180.12:53281",
    "160.238.208.198:53281",
    "168.181.161.13:53281",
    "170.0.69.242:65309",
    "153.126.195.219:80",
    "171.244.80.17:65301",
    "175.100.91.105:65205",
    "168.195.210.163:53281",
    "176.106.39.20:53281",
    "169.239.0.182:80",
    "175.100.19.243:53281",
    "168.253.201.19:53281",
    "168.234.75.119:80",
    "177.66.240.49:53281",
    "178.216.34.165:53281",
    "177.234.14.146:8080",
    "177.207.234.14:80",
    "178.22.117.153:53281",
    "178.222.228.81:53281",
    "178.211.184.196:53281",
    "178.62.28.110:8118",
    "178.22.216.35:53281",
    "177.131.51.167:53281",
    "180.234.223.18:63909",
    "181.112.138.198:65301",
    "180.178.96.61:53281",
    "181.112.152.222:65103",
    "181.112.221.182:53281",
    "180.250.65.17:8080",
    "181.112.61.50:65103",
    "181.129.33.218:62225",
    "181.193.60.194:53281",
    "168.195.209.89:53281",
    "181.30.101.242:3128",
    "181.196.50.238:65103",
    "181.196.207.66:62225",
    "181.196.145.106:65103",
    "181.112.61.186:65103",
    "173.212.202.65:80",
    "182.23.49.19:8080",
    "183.91.3.146:53281",
    "185.108.215.247:53281",
    "185.105.246.251:53281",
    "185.13.228.124:1009",
    "185.119.57.63:53281",
    "185.45.93.205:53281",
    "185.141.11.182:65103",
    "185.74.192.176:53281",
    "185.6.242.98:53281",
    "185.74.192.175:53281",
    "185.12.22.43:53281",
    "185.95.186.78:65103",
    "186.195.172.35:53281",
    "186.46.85.194:62225",
    "186.46.198.162:62225",
    "186.46.153.174:62225",
    "186.103.239.190:80",
    "186.68.85.26:53281",
    "186.215.78.3:53281",
    "187.243.251.30:65103",
    "187.49.206.162:80",
    "188.166.144.170:8118",
    "186.249.7.97:8080",
    "185.90.61.18:3128",
    "178.217.33.134:53281",
    "188.214.122.153:53281",
    "189.206.107.6:8080",
    "185.155.67.160:53281",
    "190.1.174.162:53281",
    "190.121.167.218:53281",
    "190.153.137.15:62225",
    "190.186.58.167:53281",
    "190.214.10.54:62225",
    "190.63.187.230:62225",
    "191.102.122.3:65301",
    "190.186.144.75:53281",
    "193.188.254.67:53281",
    "192.118.72.53:80",
    "194.15.122.246:53281",
    "194.177.0.74:53281",
    "193.111.177.51:80",
    "195.138.83.188:62225",
    "194.14.207.87:80",
    "195.234.87.211:53281",
    "192.198.85.158:80",
    "196.223.140.170:63909",
    "188.195.53.120:8080",
    "196.22.53.81:53281",
    "190.96.125.193:53281",
    "197.255.252.27:62225",
    "197.248.223.230:53281",
    "197.245.217.85:62225",
    "196.46.179.241:53281",
    "198.84.229.58:9999",
    "200.114.102.129:53281",
    "200.123.50.43:53281",
    "197.234.35.82:53281",
    "200.109.119.126:63909",
    "197.248.149.14:53281",
    "200.109.108.137:3128",
    "200.53.19.32:53281",
    "201.245.190.38:65301",
    "200.85.211.202:53281",
    "201.72.43.195:53281",
    "201.217.217.26:8080",
    "202.131.233.202:53281",
    "202.21.116.186:53281",
    "202.21.116.190:53281",
    "202.40.180.22:53281",
    "202.56.203.40:80",
    "202.40.177.230:53281",
    "202.79.59.173:53281",
    "202.62.12.174:53281",
    "202.69.38.68:80",
    "203.142.34.36:62225",
    "203.189.135.107:65103",
    "203.141.149.145:8080",
    "203.86.205.106:80",
    "207.204.83.22:62225",
    "188.92.214.131:80",
    "210.54.213.130:53281",
    "203.123.229.38:53281",
    "212.20.73.70:62225",
    "212.200.246.24:80",
    "212.126.107.182:62225",
    "212.56.204.6:62225",
    "213.108.18.72:53281",
    "212.49.84.71:65301",
    "213.148.166.161:53281",
    "217.30.64.26:53281",
    "217.24.160.10:3128",
    "218.201.98.196:3128",
    "218.254.1.14:80",
    "218.248.42.140:53281",
    "219.130.39.55:53281",
    "222.255.122.58:3128",
    "27.109.4.46:65309",
    "31.145.111.25:53281",
    "27.50.49.24:3128",
    "36.66.124.201:65103",
    "36.67.141.211:65103",
    "31.179.240.169:53281",
    "31.220.183.217:53281",
    "36.67.142.53:8080",
    "37.29.82.115:65103",
    "36.66.87.18:53281",
    "36.67.78.53:53281",
    "37.17.38.196:53281",
    "37.143.160.124:62225",
    "41.207.49.132:53281",
    "36.67.24.255:62225",
    "41.242.90.74:65301",
    "41.204.32.194:53281",
    "41.221.97.178:62225",
    "41.67.139.142:53281",
    "36.67.89.179:65205",
    "41.60.233.159:62225",
    "41.77.128.18:62225",
    "41.78.243.233:53281",
    "45.115.99.226:53281",
    "45.123.0.90:65301",
    "45.251.72.110:53281",
    "43.229.88.98:53281",
    "41.75.68.159:65205",
    "46.151.145.4:53281",
    "45.123.8.132:62225",
    "46.242.29.70:53281",
    "45.6.65.119:65309",
    "46.23.141.88:62225",
    "46.8.243.89:65205",
    "41.75.68.29:62225",
    "46.99.151.12:53281",
    "36.67.96.179:8080",
    "47.52.59.45:80",
    "5.197.149.233:8080",
    "41.87.3.74:62225",
    "5.61.212.42:53281",
    "52.174.89.111:80",
    "54.64.37.176:80",
    "51.15.160.216:80",
    "52.50.247.10:80",
    "51.15.86.160:80",
    "60.255.186.169:8888",
    "222.124.187.3:53281",
    "61.6.58.15:53281",
    "58.87.87.142:80",
    "60.250.72.252:8080",
    "61.6.64.73:53281",
    "61.91.235.226:8080",
    "61.6.148.142:53281",
    "62.182.207.26:53281",
    "62.99.77.124:65205",
    "64.34.21.84:80",
    "66.175.83.156:8080",
    "61.255.239.33:3129",
    "66.70.191.5:3128",
    "79.135.195.131:53281",
    "79.11.41.215:53281",
    "78.26.207.173:53281",
    "79.138.7.81:65205",
    "80.161.30.153:80",
    "80.161.30.154:80",
    "80.83.20.14:80",
    "81.163.119.84:53281",
    "81.88.198.162:53281",
    "81.89.60.26:53281",
    "82.114.90.161:53281",
    "78.163.152.22:8080",
    "82.114.94.68:53281",
    "82.21.22.60:80",
    "85.112.69.158:62225",
    "85.159.2.205:9999",
    "85.157.92.143:53281",
    "85.187.245.26:53281",
    "86.100.77.210:53281",
    "87.110.0.182:53281",
    "88.119.49.66:63909",
    "88.102.89.44:53281",
    "87.251.126.151:3128",
    "82.200.195.18:62225",
    "83.64.253.167:80",
    "87.245.154.66:80",
    "83.64.253.168:80",
    "86.109.100.80:8080",
    "91.193.130.172:53281",
    "91.209.54.37:53281",
    "91.226.35.93:53281",
    "91.225.197.197:65103",
    "91.214.62.168:53281",
    "92.115.81.82:53281",
    "91.206.111.142:53281",
    "91.194.42.51:80",
    "93.157.233.125:53281",
    "93.103.12.195:53281",
    "87.242.77.197:8080",
    "94.248.145.173:53281",
    "94.154.22.193:53281",
    "94.190.19.11:53281",
    "95.143.139.149:65205",
    "95.67.46.86:62225",
    "96.9.69.210:53281",
    "93.179.231.56:53281",
    "87.79.68.60:8080",
    "92.241.80.158:80",
    "80.161.30.155:80",
    "80.161.30.156:80",
    "80.161.30.157:80",
    "82.165.151.230:80"
]
USERAGENTS = [
    "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",
    "Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; chromeframe/12.0.742.112)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET CLR 1.1.4322; .NET4.0C; Tablet PC 2.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; FunWebProducts)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/11.0.696.57)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.1; SV1; .NET CLR 2.8.52393; WOW64; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; chromeframe/11.0.696.57)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/4.0; GTB7.4; InfoPath.3; SV1; .NET CLR 3.1.76908; WOW64; en-US)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; FunWebProducts)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/11.0.696.57)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; chromeframe/11.0.696.57)"
]


def get_html(url):
    proxy = {'http': 'http://' + choice(PROXIES)}
    useragent = {'User-Agent': choice(USERAGENTS)}
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_html1(url):
    r = requests.get(url)
    return r.text


def get_categories_from_db(url):
    html = get_html1(url)
    return json.loads(html)


def get_data(context):
    product_dict = {
        'id': context['id']
    }
    cont = {}
    try:
        url = context['url']
        product_id = url.split('-c')[-1].split('p')[-1].split('.html')[0]
        colour_id = url.split('.html?cS=')[-1]
        category_id = url.split('-c')[-1].split('p')[0]
        product_json_url = 'https://www.pullandbear.com/itxrest/2/catalog/store/25009521/20309411/category/0/product/%s/detail?languageId=-43&appId=1' % product_id
        html = get_html(product_json_url)
        json_data = json.loads(html)
        cont['stock'] = True
        static = 'https://static.pullandbear.net/2/photos'
        medias = json_data['bundleProductSummaries'][0]['detail']['xmedia']
        images = []
        for media in medias:
            if media['colorCode'] == str(colour_id):
                path = static + media['path'] + '/'
                m = media['path'].split('/')[-3:]
                t = ''
                for n in m:
                    t = t + n
                for xmedia in media['xmediaItems'][0]['medias']:
                    split = xmedia['idMedia'].split('_')
                    z = t
                    for s in split[1:]:
                        z = z + '_' + s
                    image = path + z + '8.jpg?t=' + str(
                        xmedia['timestamp'])
                    images.append(image)
                    z = ''
                break

        image_text = ''
        for image in images:
            image_text = image_text + image + ' '
        cont['images'] = image_text
        product_sizes = []
        for color in json_data['bundleProductSummaries'][0]['detail']['colors']:
            if color['id'] == str(colour_id):
                cont['colour'] = color['name']
                product_sizes = color['sizes']
                break
        stock_url = 'https://www.pullandbear.com/itxrest/2/catalog/store/25009521/20309411/product/%s/stock?languageId=-43&appId=1' % product_id
        stock_json = get_html(stock_url)
        stock_data = json.loads(stock_json)
        sizes = []
        price = 0
        for stock in stock_data['stocks']:
            if stock['productId'] == int(product_id):
                for product_stock in stock['stocks']:
                    for product_size in product_sizes:
                        if product_size['sku'] == product_stock['id']:
                            stock_bool = False
                            if product_stock['availability'] == 'in_stock':
                                stock_bool = True
                            size = {
                                "value": product_size['name'],
                                'stock': stock_bool
                            }
                            sizes.append(size)
                            if int(product_size['price']) / 100 > price:
                                price = int(product_size['price']) / 100
            break
        cont['sizes'] = sizes
        cont['selling_price'] = price
        cont['discount_price'] = price
        cont['original_price'] = price
    except:
        cont = None
        pass
    product_dict['product'] = cont
    return product_dict


def main():
    url = 'https://magicbox.izishop.kg/api/v1/project/update/links/?brand=PLLBR'
    # data_url = 'https://www.pullandbear.com/tr/kad%C4%B1n/giyim/t-shirtler/basic-fitilli-ask%C4%B1l%C4%B1-body-c29020p502184763.html?cS=612'
    # print(get_data({'url': data_url, 'id': 1}))
    links = get_categories_from_db(url)
    length = (len(links))
    print(length)
    ranges = length // 10 + 1
    all_products = []
    get_data(links[0])
    for i in range(ranges):
        range_links = (links[i * 10: (i + 1) * 10])
        if range_links:
            with Pool(20) as p:
                data = (p.map(get_data, range_links))
                all_products.extend(data)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url,
                          data=json.dumps(all_products), headers=headers)
        print(r.status_code)
        all_products = []
        time.sleep(3)


if __name__ == '__main__':
    main()