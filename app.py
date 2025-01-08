from flask import Flask, render_template
from scraper import fetch_articles
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    url = "https://sea.mashable.com/article"
    date_limit = datetime(2024, 12, 1)  # Y/M/D to catch the article until the date
    articles = fetch_articles(url, date_limit)
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
