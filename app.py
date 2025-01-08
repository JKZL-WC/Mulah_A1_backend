import os
from flask import Flask, render_template, jsonify
from scraper import fetch_articles
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

@app.route("/")
def home():
    try:
        # Target URL for scraping
        url = "https://sea.mashable.com/article"
        # Date limit for filtering articles
        date_limit = datetime(2024, 12, 1)
        # Fetch articles using the scraper
        articles = fetch_articles(url, date_limit)
        return render_template("index.html", articles=articles)
    except Exception as e:
        # Return error response if scraping fails
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Get the dynamic PORT provided by Render, default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Run Flask app on 0.0.0.0 for external access
    app.run(host="0.0.0.0", port=port)
