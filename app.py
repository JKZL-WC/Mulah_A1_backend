from flask import Flask, render_template
from scraper import fetch_articles
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    try:
        url = "https://sea.mashable.com/article"
        date_limit = datetime(2024, 12, 1)
        articles = fetch_articles(url, date_limit)
        return render_template('index.html', articles=articles)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
