from selenium import webdriver
import time
import pickle
from bs4 import BeautifulSoup
import csv
import datetime


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('headless')

driver = webdriver.Chrome(executable_path="/home/bot_parser/chromedriver", options=chrome_options)

current_date = datetime.datetime.now().strftime('%m-%d')

def parser_magnit():
    url = f'https://magnit.ru/promo-catalog/'

    driver.get(url=url)
    print('подключились')


    for cookie in pickle.load(open('cookie_spb', 'rb')):
        driver.add_cookie(cookie)
    # pickle.dump(driver.get_cookies(), open("cookie_spb", "wb"))
    # print('куки записаны')

    driver.refresh()

    soup = BeautifulSoup(driver.page_source, 'lxml')

    lists = soup.find('nav', class_='pl-pagination__pager').find_all('li')[5].find('span', class_='pl-button__icon').text

    with open(f'magnit_{current_date}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Продукт',
                'Старая цена',
                'Новая цена',
                'Процент скидки',
            )
        )

    for i in range(1, int(lists)+1):

        driver.get(url=f'https://magnit.ru/promo-catalog/?page={i}')
        driver.refresh()
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'lxml')

        cards = soup.find_all('div', class_='pl-stack-item pl-stack-item_size-6 pl-stack-item_size-4-m pl-stack-item_size-3-ml unit-catalog__stack-item')

        for card in cards:

            if card.find('span', class_='pl-text unit-catalog-product-preview-prices__sale') and card.find('div', class_='pl-label__value-text'):
                product = card.find('div', class_="pl-text unit-catalog-product-preview-title").text

                prise_new = card.find('span', class_='pl-text unit-catalog-product-preview-prices__regular with-sale').find('span').text

                prise_old = card.find('span', class_='pl-text unit-catalog-product-preview-prices__sale').find('span').text

                sale = card.find('div', class_='pl-label__value-text').text

                # print(product, prise_old, prise_new, sale)

                with open(f'magnit_{current_date}.csv', 'a', encoding='utf-8') as file:
                    writer = csv.writer(file)

                    writer.writerow(
                        (
                            product,
                            prise_old,
                            prise_new,
                            sale,
                        )
                    )

        print(f'[X] страницы {i} отсканирована')
    print('Файл успешно записан')

    return f'magnit_{current_date}.csv'


def collect_data():
    parser_magnit()


if __name__ == "__main__":
    collect_data()
