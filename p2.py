import time
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_title(soup):
    try:
        name = []
        for item in soup.find_all("h5", attrs={"class":'mt-3 mb-2 px-1'}):
            text = item.get_text(strip=True)
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



def get_data(p):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    URL = "https://topai.tools/next?p=" + str(p) + "&q=main&kw=&sort=0&"

    webpage = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, "html.parser")

    data = {
        "Tool Name": get_title(soup),
        "Tool URL": get_url(soup),
        "Pricing": get_price(soup),
        "Tags": get_tags(soup),
        "Uses": get_uses(soup)
    }

    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    p = 223
    data = pd.DataFrame()

    for i in range(1, p + 1):
        print(f"Scraping data for p={i}...")
        dfp = get_data(i)
        data = pd.concat([data, p], ignore_index=True)
        time.sleep(1)

    data.to_excel("data.xlsx", index=False)