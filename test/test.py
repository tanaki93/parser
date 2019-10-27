import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    href = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = href.split('=')[1].split('&')[0]
    return int(total_pages)


import csv


def write_csv(data):
    with open('test.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'], data['price'], data['metro'], data['url']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')
    for ad in ads:
        try:
            title = ad.find('div', class_='description').find('h3').text.strip()
        except:
            title = ''
        try:
            url = 'https://avito.ru' + ad.find('div', class_='description').find('h3').find(
                'a'
            ).get('href')
        except:
            url = ''
        try:
            price = ad.find('div', class_='about').text.strip()
        except:
            price = ''
        try:
            metro = ad.find('div', class_='data').find_all('p')[-1].text.strip()
        except:
            metro = ''
        data = {
            'title': title,
            'url': url,
            'price': price,
            'metro': metro
        }
        write_csv(data)


def main():
    url = 'https://www.avito.ru/moskva/telefony?q=htc'
    base_url = 'https://www.avito.ru/moskva/telefony?'
    page_part = 'p='
    query_part = '&q=htc'
    html = get_html(url)
    total_pages = get_total_pages(html)
    for i in range(1, 3):
        url_gen = base_url + page_part + str(i) + query_part
        get_page_data(get_html(url_gen))


if __name__ == '__main__':
    main()
