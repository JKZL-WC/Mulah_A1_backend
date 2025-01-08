from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_articles(url, date_limit):
    # Setup Selenium WebDriver with headers
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Set custom headers
    driver.execute_cdp_cmd(
        "Network.setExtraHTTPHeaders",
        {"headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }}
    )

    driver.get(url)

    articles = []
    stop_clicking = False  # Stop clicking when date limit is reached

    try:
        while not stop_clicking:
            # Use BeautifulSoup to parse the page
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            for article in soup.find_all('li', class_='blogroll ARTICLE'):
                # Extract details
                link_tag = article.find('a', href=True)
                title_tag = article.find('div', class_='caption')
                description_tag = article.find('div', class_='deck')
                date_tag = article.find('time', class_='datepublished')

                link = link_tag['href'] if link_tag else None
                title = title_tag.text.strip() if title_tag else None
                description = description_tag.text.strip() if description_tag else None
                published_date = date_tag.text.strip() if date_tag else None

                # Convert date
                try:
                    date_obj = datetime.strptime(published_date, "%b. %d, %Y") if published_date else None
                except ValueError:
                    date_obj = None

                # Stop if the date exceeds the limit
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

            # Stop the loop if no "Show More" button
            if stop_clicking:
                break

            try:
                show_more_button = driver.find_element(By.ID, "showmore")
                show_more_button.click()
            except Exception as e:
                print("No more 'Show More' button or error:", e)
                break

    finally:
        driver.quit()

    # Sort articles by date descending
    articles.sort(key=lambda x: x['date'], reverse=True)
    return articles
