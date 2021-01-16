from flask import Flask, render_template, request, redirect, url_for
import feedparser

app = Flask(__name__)

URL = r'http://feeds.bbci.co.uk/news/rss.xml'


@app.route('/news')
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('base.html')
    else:
        name = request.form['name']
        return render_template('base.html', name=name)


@app.route('/sign/')
def sign():
    return render_template('sign.html')


@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    password = request.form['password']
    if name == 'borko' and password == 'test':
        return render_template('comments.html')
    else:
        return redirect(url_for('sign'))


if __name__ == '__main__':
    app.run(debug=True)
