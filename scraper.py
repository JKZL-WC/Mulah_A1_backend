from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import time

def fetch_articles(url, date_limit):
    # setup Selenium WebDriver
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    articles = []
    stop_clicking = False  # check to stop to press

    try:
        while not stop_clicking:
            # use BeautifulSoup to run the page
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            for article in soup.find_all('li', class_='blogroll ARTICLE'):
                # link
                link_tag = article.find('a', href=True)
                link = link_tag['href'] if link_tag else None

                # title
                title_tag = article.find('div', class_='caption')
                title = title_tag.text.strip() if title_tag else None

                # description
                description_tag = article.find('div', class_='deck')
                description = description_tag.text.strip() if description_tag else None

                # Date
                date_tag = article.find('time', class_='datepublished')
                published_date = date_tag.text.strip() if date_tag else None

                # change to datetime
                try:
                    date_obj = datetime.strptime(published_date, "%b. %d, %Y") if published_date else None
                except ValueError:
                    date_obj = None

                # stop if the date in over
                if date_obj and date_obj < date_limit:
                    stop_clicking = True
                    break

                if date_obj and date_obj >= date_limit:
                    articles.append({
                        'title': title,
                        'description': description,
                        'link': link,
                        'date': date_obj
                    })

            # stop to loop
            if stop_clicking:
                break

            # press "Show More"
            try:
                show_more_button = driver.find_element(By.ID, "showmore") 
                show_more_button.click()
                # time.sleep(2)
            except Exception as e:
                print("No more 'Show More' button or error:", e)
                break

    finally:
        driver.quit()

    # sort by date desc
    articles.sort(key=lambda x: x['date'], reverse=True)
    return articles