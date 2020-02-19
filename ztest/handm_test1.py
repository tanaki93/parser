from bs4 import BeautifulSoup

from koton.parse_category import get_html


def get_data():
    html = get_html('https://www2.hm.com/tr_tr/erkek/urune-gore-satin-al/ayakkabi.html')
    soup = BeautifulSoup(html, 'lxml')
    menu = soup.find('div', class_='sidebar-plus-content').find('aside').find('nav',
                                                                              class_='secondary-nav') \
        .find('ul', id='menu-links').find_all('li', class_='list-group')
    for i in menu:
        menu_item = None
        try:
            menu_item = i.find('strong', class_='list-group-title is-opened')
        except:
            pass
        if menu_item is not None:
            ul = (i.find('ul', class_='menu').find('li', class_='list-group').find('ul').find_all('li'))
            categories = [
                {'category': j.find('a').text.strip(), 'link': 'https://www2.hm.com'
                                                               + j.find('a')['href']} for j
                in ul]
            print(categories)

    return []


def main():
    get_data()


if __name__ == '__main__':
    main()
