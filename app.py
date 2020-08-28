from flask import Flask
from flask import render_template
from flask import request
from Scraper import fox_article_info , foxArticleTextScraper, cnn_article_info, cnnArticleTextScraper, nbc_article_info, nbcArticleTextScraper
from ML import predictor
#python -m flask run
app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html', headline = fox_article_info )

@app.route('/fox_links/')
def fox_links():
    return render_template('fox_links.html', headline = fox_article_info )

@app.route('/fox_validity/', methods = ('POST', 'GET'))
def fox_validity():
    url = request.form['url']
    pred = predictor(foxArticleTextScraper(url))
    if pred == 0:
        pred = "Likely true information without intention of misleading audience"
    elif pred == 1:
        pred = "Likely fake or dishonest or choicefully worded information to mislead audience"
    return render_template('fox_links2.html', headline = fox_article_info , pred = pred, url = url)

########################################################   CNN

@app.route('/cnn_links/')
def cnn_links():
    #cant use fox_links.html because it uses foxArticleTextScraper and not CNN one to make prediciton, they have different html so they need their own text scraper to be sent to
    return render_template('cnn_links.html', headline = cnn_article_info)

@app.route('/cnn_validity/',  methods = ('POST', 'GET'))
def cnn_validity():
    url = request.form['url']
    pred = predictor(cnnArticleTextScraper(url))
    if pred == 0:
        pred = "Likely true information without intention of misleading audience"
    elif pred == 1:
        pred = "Likely fake or dishonest or choicefully worded information to mislead audience"
    return render_template('cnn_links2.html', headline = cnn_article_info, pred = pred, url = url)

##########################################################  NBC

@app.route('/nbc_links/')
def nbc_links():
    #cant use fox_links.html because it uses foxArticleTextScraper and not CNN one to make prediciton, they have different html so they need their own text scraper to be sent to
    return render_template('nbc_links.html', headline = nbc_article_info)

@app.route('/nbc_validity/',  methods = ('POST', 'GET'))
def nbc_validity():
    url = request.form['url']
    pred = predictor(nbcArticleTextScraper(url))
    if pred == 0:
        pred = "Likely true information without intention of misleading audience"
    elif pred == 1:
        pred = "Likely fake or dishonest or choicefully worded information to mislead audience"
    return render_template('nbc_links2.html', headline = nbc_article_info, pred = pred, url = url)

