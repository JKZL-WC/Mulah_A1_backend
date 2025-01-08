from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import time

def fetch_articles(url, date_limit):
    articles = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        while True:
            # Extract current page content
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            page_articles = []

            for article in soup.find_all('li', class_='blogroll ARTICLE'):
                link_tag = article.find('a', href=True)
                title_tag = article.find('div', class_='caption')
                description_tag = article.find('div', class_='deck')
                date_tag = article.find('time', class_='datepublished')

                link = link_tag['href'] if link_tag else None
                title = title_tag.text.strip() if title_tag else None
                description = description_tag.text.strip() if description_tag else None
                published_date = date_tag.text.strip() if date_tag else None

                try:
                    date_obj = datetime.strptime(published_date, "%b. %d, %Y") if published_date else None
                except ValueError:
                    date_obj = None

                # Stop if article date is earlier than the date limit
                if date_obj and date_obj < date_limit:
                    browser.close()
                    articles.extend(page_articles)
                    articles.sort(key=lambda x: x['date'], reverse=True)
                    return articles

                # Append formatted date as string
                page_articles.append({
                    'title': title,
                    'description': description,
                    'link': link,
                    'date': date_obj.strftime('%Y-%m-%d') if date_obj else "Unknown"
                })

            # Append current page articles to all articles
            articles.extend(page_articles)

            # Try clicking "Show More" button to load more articles
            try:
                page.click("#showmore")
                #time.sleep(2)  # Wait for new content to load
            except:
                print("No more 'Show More' button.")
                break

        browser.close()

    # Sort articles by date descending
    articles.sort(key=lambda x: x['date'], reverse=True)
    return articles
