import os
import subprocess
from flask import Flask, render_template, jsonify
from scraper import fetch_articles
from datetime import datetime

# Ensure Playwright browsers are installed
if not os.path.exists("/opt/render/.cache/ms-playwright"):
    subprocess.run(["playwright", "install", "chromium"], check=True)

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    try:
        url = "https://sea.mashable.com/article"
        date_limit = datetime(2024, 12, 1)
        articles = fetch_articles(url, date_limit)
        return render_template("index.html", articles=articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
