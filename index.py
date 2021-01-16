from flask import Flask
import feedparser

app = Flask(__name__)

URL = r'http://feeds.bbci.co.uk/news/rss.xml'


@app.route('/')
def get_news():
    parser = feedparser.parse(URL)
    first_article = parser['entries'][0]
    return f"""<html>
    <head></head>
    <body>
    <h1>Software feed</h1>
    <p><b>{first_article.get('title')}</b></p>
    <p>{first_article.get('summary')}</p>
    <a href='{first_article.get('link')}'>Link</a>
    </body>
    </html>
    """


if __name__ == '__main__':
    app.run(debug=True)
