from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import feedparser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\borko\Desktop\flask\foo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

'''
from index import db
db.create_all()

'''


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))


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
        result = Comments.query.all()
        return render_template('base.html', result=result)
    else:
        name = request.form['name']
        signiture = Comments(name=name)
        db.session.add(signiture)
        db.session.commit()
        return redirect(url_for('index'))


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
