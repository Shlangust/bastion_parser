import time
from time import sleep

from openpyxl import load_workbook
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import none_of
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_page():
    driver = webdriver.Chrome()
    driver.get('https://bast.ru/products')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "stretched-link"))
    )
    with open("index.html", "w", encoding='utf-8') as file:
        file.write(driver.page_source)

def test(file):
    seen_links = set()

    data = []

    driver = webdriver.Chrome()

    with open(file,encoding='utf-8') as f:
        scr = f.read()
    soup = bs(scr,'lxml')
    items =soup.find_all('a',class_='stretched-link')
    urls = []
    for item in items:
        item_url = 'https://bast.ru/' + item.get('href')
        urls.append(item_url)

    for url in urls:
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "subcategory-menu"))
            )
            source = driver.page_source
            soup = bs(source, 'lxml')
            subcategories = soup.find_all('a', class_='subcategory-menu')
            subcategory_links = []
            for category in subcategories:
                subcategory_links.append('https://bast.ru/' + category.get('href'))
            for subcategory in subcategory_links:
                driver.get(subcategory)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "link-unset"))
                )
                source = driver.page_source
                soup = bs(source, 'lxml')
                product = soup.find_all('div',class_='flex-grow-1 card-body')
                product_links = []
                for category in product:
                    product_links.append('https://bast.ru/' + category.find('a',class_='link-unset').get('href'))
                for product_link in product_links:
                    driver.get(product_link)
                    source = driver.page_source
                    soup = bs(source, 'lxml')

                    name = soup.find('div', class_='col-lg-9 order-1 order-lg-2').find('h1')
                    price = soup.find('p', class_='product-price')

                    if name != None:
                        name = name.text
                    if price != None:
                        price = price.text
                    print(name, price,product_link)
                    characteristics_raw = soup.find('div', class_='row align-items-start').find_all('li')
                    characteristics = []
                    for i in characteristics_raw:
                        characteristics.append(i.text)

                    data.append({
                        "Имя": name,
                        "цена": price,
                        "характеристики": ', '.join(characteristics),
                        "ссылка на товар": product_link
                    })
        except:
            # try:
            #     WebDriverWait(driver, 10).until(
            #         EC.presence_of_element_located((By.CLASS_NAME, "link-unset"))
            #     )
                source = driver.page_source
                soup = bs(source, 'lxml')
                product = soup.find_all('a', class_='link-unset')
                product_links = []
                for category in product:
                    product_links.append('https://bast.ru/' + category.get('href'))
                for product_link in product_links:
                    time.sleep(0.1)
                    driver.get(product_link)
                    source = driver.page_source
                    soup = bs(source, 'lxml')

                    name = soup.find('div', class_='col-lg-9 order-1 order-lg-2').find('h1')
                    price = soup.find('p', class_='product-price')

                    if name != None:
                        name = name.text
                    if price != None:
                        price = price.text

                    characteristics_raw = soup.find('div', class_='row align-items-start').find_all('li')
                    characteristics = []
                    for i in characteristics_raw:
                        characteristics.append(i.text)
                    print(name,product_link,product_link)
                    if product_link not in seen_links:
                        seen_links.add(product_link)
                        data.append({
                            "Имя": name,
                            "цена": price,
                            "характеристики": ', '.join(characteristics),
                            "ссылка на товар": product_link
                        })
            # except Exception as e:
            #     print(e)
            #     time.sleep(1000000000)
            # finally:
            #     df = pd.DataFrame(data)
            #     file_name = f"data.xlsx"
            #     df.to_excel(file_name, index=False)
    df = pd.DataFrame(data)
    file_name = f"data.xlsx"
    df.to_excel(file_name, index=False)

import time
from datetime import datetime


def wait_until(hour, minute):
    while True:
        now = datetime.now()
        if now.hour == hour and now.minute == minute:
            return
        time.sleep(30)  # Проверяет каждые 30 секунд

def main():
    while True:
        wait_until(18, 5)
        get_page()
        test('index.html')
        time.sleep(60)  # Ждёт минуту, чтобы не запустилось снова в ту же минуту

if __name__ == "__main__":
    main()