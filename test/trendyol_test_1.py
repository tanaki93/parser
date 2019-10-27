import time
from random import randint

from bs4 import BeautifulSoup
from selenium import webdriver


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup)


def main():
    driver = webdriver.Chrome(executable_path=r'C:\chromedriver.exe')
    driver.get("https://www.trendyol.com/mango")
    last_height = driver.execute_script("return document.body.scrollHeight")
    count = 0
    num = 0
    while True:
        num += 1
        count += randint(4000, 4500)
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, %s);" % count)

        # Wait to load page
        time.sleep(0.4)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(new_height, last_height)
        if new_height == last_height:
            break
        last_height = new_height
    elem = driver.page_source
    get_total_pages(elem)


if __name__ == '__main__':
    main()
