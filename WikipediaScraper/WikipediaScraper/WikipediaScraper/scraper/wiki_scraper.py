from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def scrape_infobox(country):
    url = f"https://en.wikipedia.org/wiki/Demographics_of_{country}"
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    infobox = soup.find('table', {'class': 'infobox'})
    data_list = []

    if infobox:
        rows = infobox.find_all('tr')
        for row in rows:
            th = row.find('th')
            td = row.find('td')
            if th and td:
                label = th.get_text(strip=True)
                value = td.get_text(strip=True).replace('\xa0', ' ')
                data_list.append({'Field': label, 'Value': value})

    return pd.DataFrame(data_list)
