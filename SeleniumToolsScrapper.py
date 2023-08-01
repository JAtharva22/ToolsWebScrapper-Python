import json
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_title(soup):
    try:
        name = []
        for item in soup.find_all("h5", attrs={"class":'mt-3 mb-2 px-1'}):
            target_a = item.select_one("a")

            # Extract the text within the <a> element
            text = target_a.get_text(strip=True)
            name.append(text)
        print(len(name))
        return name
    except AttributeError:
        return []

def get_price(soup):
    try:
        price = []
        for item in soup.find_all("span", attrs={"class":'badge float-end bg-black mr-2 pricing-badge'}):
            text = item.get_text(strip=True)
            if text == '' :
                price.append("Unknown")
            else:
                price.append(text)
        print(len(price))
        return price
        # return name
    except AttributeError:
        return []

def get_url(soup):
    try:
        url = []
        for item in soup.find_all("a", attrs={"class":'mx-2 rounded p-1'}  ):
            text = item['href']
            url.append(text)
        print(len(url))
        return url
    except AttributeError:
        return []

def get_tags(soup):
    try:
        tag = []
        for item in soup.find_all("i", attrs={"class":'bi bi-heart float-end icons'}):
            tag.append(item['data-tags'])
        print(len(tag))
        return tag
    except AttributeError:
        return []

def get_uses(soup):
    try:
        use = []
        for item in soup.find_all("p", class_=lambda x: x and "font-weight-lighter" in x):
            use.append(item.get_text())
        print(len(use))
        return use
    except AttributeError:
        return []

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://topai.tools/browse#")
time.sleep(2)  
scroll_pause_time = 1 
screen_height = driver.execute_script("return window.screen.height;")   
i = 1


while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    if i > 1300:
        break
    if screen_height * i > scroll_height:
        break

soup = BeautifulSoup(driver.page_source, "html.parser")


data = {
    "Tool Name": get_title(soup),
    "Tool URL": get_url(soup),
    "Pricing": get_price(soup),
    "Tags": get_tags(soup),
    "Uses": get_uses(soup)
}

df = pd.DataFrame(data)

df.to_excel("data.xlsx",index=False)

driver.quit()  
