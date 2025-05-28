import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
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

def get_links(file):
    with open(file,encoding='utf-8') as f:
        scr = f.read()
    soup = bs(scr,'lxml')
    items =soup.find_all('a',class_='stretched-link')
    urls = []
    for item in items:
        item_url = 'https://bast.ru/' + item.get('href')
        urls.append(item_url)

    return urls
def go_to_category(link):
    driver = webdriver.Chrome()
    driver.get(link)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "subcategory-menu"))
    )
    source = driver.page_source
    soup = bs(source,'lxml')
    subcategories = soup.find_all('a',class_='subcategory-menu')
    subcategory_links = []
    for category in subcategories:
        subcategory_links.append('https://bast.ru/' + category.get('href'))
    return subcategory_links
def go_to_subcategory(link):
    driver = webdriver.Chrome()
    driver.get(link)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "link-unset"))
    )
    source = driver.page_source
    soup = bs(source, 'lxml')
    product = soup.find_all('a', class_='link-unset')
    product_links = []
    for category in product:
        product_links.append('https://bast.ru/' + category.get('href'))
    return product_links
def in_product(link):
    driver = webdriver.Chrome()
    driver.get(link)

    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "row align-items-start"))
    # )
    source = driver.page_source
    soup = bs(source, 'lxml')
    characteristics_raw = soup.find('div',class_='row align-items-start').find_all('li')
    characteristics = []
    for i in characteristics_raw:
        characteristics.append(i.text)
    print(characteristics)



get_page()
links = get_links('index.html')
print(links[5])
slincks = go_to_category(links[5])
a = go_to_subcategory(slincks[3])[18]
print(a)
in_product(a)

