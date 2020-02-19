from time import sleep

from koton.parse_category import get_html1


def main():
    url = 'http://188.120.242.218:8089/api/v1/post/'
    # url = 'http://127.0.0.1:8000/api/v1/project/brands/handm/'
    for i in range(1, 30):
        html = get_html1(url+str(i)+'/')
        print(i, html)
        sleep(3)


if __name__ == '__main__':
    main()