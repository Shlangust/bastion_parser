import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

driver = webdriver.Chrome()


def parse_product_page(url):
    driver.get(url)
    soup = bs(driver.page_source, 'lxml')
    name_tag = soup.find('div', class_='col-lg-9 order-1 order-lg-2').find('h1')
    price_tag = soup.find('p', class_='product-price')
    name = name_tag.text if name_tag else ''
    price = price_tag.text if price_tag else ''
    characteristics_div = soup.find('div', class_='row align-items-start')
    characteristics = []

    if characteristics_div:
        characteristics_raw = characteristics_div.find_all('li') or characteristics_div.find_all('p')
        characteristics = [elem.text for elem in characteristics_raw]
    return {
        "Имя": name,
        "цена": price,
        "характеристики": ', '.join(characteristics),
        "ссылка на товар": url
    }

def test():
    driver.get('https://bast.ru/products')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "stretched-link"))
    )
    data = []
    soup = bs(driver.page_source,'lxml')
    items =soup.find_all('a',class_='stretched-link')
    urls = ('https://bast.ru/' + item.get('href') for item in items)
    for url in urls:
        driver.get(url)
        soup = bs(driver.page_source, 'lxml')
        subcategory_links = [
            'https://bast.ru/' + a.get('href')
            for a in soup.find_all('a', class_='subcategory-menu') if a.get('href')
        ]
        if subcategory_links:
            for subcategory in subcategory_links:
                driver.get(subcategory)
                soup = bs(driver.page_source, 'lxml')

                product_links = set('https://bast.ru/' + link['href'] for link in soup.find_all('a', class_='link-unset'))

                for product_link in product_links:
                    data.append(parse_product_page(product_link))
        else:
            source = driver.page_source
            soup = bs(source, 'lxml')
            product_links = set('https://bast.ru/' + link['href'] for link in soup.find_all('a', class_='link-unset'))
            for product_link in product_links:
                data.append(parse_product_page(product_link))

    df = pd.DataFrame(data)
    df.to_excel("data.xlsx", index=False)
def wait_until(hour, minute):
    while True:
        now = datetime.now()
        if now.hour == hour and now.minute == minute:
            return
        time.sleep(30)

def main():
    while True:
        wait_until(1, 0)
        test()
        time.sleep(60)

if __name__ == "__main__":
    main()