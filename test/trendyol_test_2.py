import json

import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    href = soup.find('div', class_='dscrptn')
    return int(href.text.split(' ')[-3])


# def get_product_count(html):
#     soup = BeautifulSoup(html, 'lxml')
#     products = soup.find('div', class_='prdct-cntnr-wrppr').find_all('div', class_='p-card-wrppr')
#     print(len(products))

def get_href(html):
    return html.get('href')


def get_links(html):
    soup = BeautifulSoup(html, 'lxml')
    products = [get_href(i) for i in soup.find_all('a', class_='p-card-chldrn-cntnr')]
    # print(products)
    return products


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    href = soup.find('div', id='container').select('script')[1].text.split('window.__SEARCH_APP_INITIAL_STATE__ = ')[
        -1].strip()
    print(href)
    href = (json.loads(href[:-1]))
    return href


def open_one_page():
    url = "https://www.trendyol.com/mango-woman/kadin-siyah-kapakli-canta-p-6587327?boutiqueId=333091&merchantId=104723"
    html = get_html(url)
    data = get_data(html)
    with open('item.json', 'w') as outfile:
        json.dump(data, outfile)


def get_first_page():
    url = "https://www.trendyol.com/mango?pi=1"
    html = get_html(url)
    data = get_data(html)
    with open('first.json', 'w') as outfile:
        json.dump(data, outfile)


def get_second_page():
    url = "https://www.trendyol.com/mango?pi=2"
    html = get_html(url)
    data = get_data(html)
    with open('second.json', 'w') as outfile:
        json.dump(data, outfile)


def main():
    url = 'https://www.trendyol.com/mango'
    page_query = '?pi='
    # html = get_html(url)
    # pages = get_total_pages(html)
    # print(pages)
    # all_links = []
    # for i in range(1, 2):
    #     data = get_html(url + page_query + str(i))
    #     links = get_links(data)
    #     all_links.extend(links)
    #
    # with open('links.json', 'w') as outfile:
    #     json.dump(all_links, outfile)
    get_first_page()
    get_second_page()


if __name__ == '__main__':
    main()
