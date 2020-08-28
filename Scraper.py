import requests
from bs4 import BeautifulSoup
import re
import lxml

fox_article_info = []
cnn_article_info = []
nbc_article_info = []

def scrapeFoxSite():
    fox = 'https://www.foxnews.com/'
    fox_page = requests.get(fox)
    fox_soup = BeautifulSoup(fox_page.text, 'html.parser')
    #only get 15 articles so pc doesnt open 140 url's
    #use regExpression to find all articles then send them over to foxArticleHeadlineUrlScraper() for information/data cleaning
    fox_article = fox_soup.find_all('article', class_=re.compile(r'article story'))
    foxArticleHeadlineUrlScraper(fox_article)


#put article url's and titles into a list of dictionaries
def foxArticleHeadlineUrlScraper(articles):
    for item in articles:
        headline = item.find('h2').getText()
        url = item.find('h2').find('a').get('href')
        info = {
        'headline': headline,
        'url' : url
        }
        fox_article_info.append(info)
    #remove video links and non article links eg clean data
    for i in range(len(fox_article_info)):
        if 'video' in fox_article_info [i]['url']:
            fox_article_info [i].clear()
        elif 'watch' in fox_article_info [i]['url']:
            fox_article_info [i].clear()
        elif '?' in fox_article_info [i]['url']:
            fox_article_info [i].clear()
    #remove empty dictionaries left from cleaning article link data
    while {} in fox_article_info :
        fox_article_info .remove({})

#get text from article for ML predictor
def foxArticleTextScraper(url):
    #get url's without video going
        article_page = requests.get(url)
        article_soup = BeautifulSoup(article_page.text, 'html.parser')
        article_text = article_soup.find(class_='article-body').get_text()
        return article_text
        #print(article_text)

scrapeFoxSite()


#scrapeFoxSite()
##############################################      CNN



def scrapeCnnSite():
    i = 0
    #cnn gets its html from a javascript call so I have to directly access the links that the JS calls this took a while to find sorting through chrome dev network tools
    cnn = ['https://www.cnn.com/data/ocs/section/index.html:homepage1-zone-1/views/zones/common/zone-manager.izl', 'https://www.cnn.com/data/ocs/section/index.html:homepage2-zone-1/views/zones/common/zone-manager.izl', 'https://www.cnn.com/data/ocs/section/index.html:homepage3-zone-1/views/zones/common/zone-manager.izl', 'https://www.cnn.com/data/ocs/section/index.html:homepage4-zone-1/views/zones/common/zone-manager.izl', 'https://www.cnn.com/data/ocs/section/index.html:homepage4-zone-1/views/zones/common/zone-manager.izl']
    for items in cnn:
        cnn_page = requests.get(cnn[i])
        cnn_soup = BeautifulSoup(cnn_page.text, 'html.parser')
        i += 1
        #only get 15 articles so pc doesnt open 140 url's
        #gets each article one at a time then pass them to the article scraper
        cnn_article = cnn_soup.find_all('h3', class_=re.compile(r'headline'))
        cnnArticleHeadlineUrlScraper(cnn_article)


def cnnArticleHeadlineUrlScraper(cnn_article):
    i = 0
    for a in cnn_article:
        cnn_article_headline = cnn_article[i].find('span').get_text()
        cnn_article_url = cnn_article[i].find('a').get('href')

        i += 1
        info = {
            'headline': cnn_article_headline,
            'url': 'https://www.cnn.com/'+ cnn_article_url[3:-2]
            # remove first and last 3 chars from url string because cnn has in in some weird javascript thing
        }
        cnn_article_info.append(info)
    #remove video links and non article links eg clean data
    for i in range(len(cnn_article_info)):
        if 'video' in cnn_article_info[i]['url']:
            cnn_article_info[i].clear()
        elif 'watch' in cnn_article_info[i]['url']:
            cnn_article_info[i].clear()
        elif '?' in cnn_article_info[i]['url']:
            cnn_article_info[i].clear()
        elif 'Live updates' in cnn_article_info[i]['headline']:
            cnn_article_info[i].clear()
    #remove empty dictionaries left from cleaning article link data
    while {} in cnn_article_info:
        cnn_article_info.remove({})

def cnnArticleTextScraper(url):
    article_page = requests.get(url)
    article_soup = BeautifulSoup(article_page.text, 'lxml')
    article_text = article_soup.find('div', class_=re.compile(r'l-container')).get_text()
    #clean text with regex
    article_text = re.sub(r'^.*?\(CNN\)', '', article_text)
    return article_text



scrapeCnnSite()


####################################################################        MSNBC


def scrapeNbcSite():
    nbc = 'https://www.nbcnews.com/'
    nbc_page = requests.get(nbc)
    nbc_soup = BeautifulSoup(nbc_page.text, 'html.parser')
    #gets each article one at a time then pass them to the article scraper
    #get big and small articles
    nbc_article = nbc_soup.find_all('h2', class_='tease-card__headline tease-card__title relative') + nbc_soup.find_all('h3', class_='related-content__headline')
    nbcArticleHeadlineUrlScraper(nbc_article)



def nbcArticleHeadlineUrlScraper(nbc_article):
    i = 0
    for a in nbc_article:
        nbc_article_headline = nbc_article[i].find('a').get_text()
        nbc_article_url = nbc_article[i].find('a').get('href')

        i += 1
        info = {
            'headline': nbc_article_headline,
            'url': nbc_article_url
        }
        nbc_article_info.append(info)
    #remove video links and non article links eg clean data nbc doesnt contain videos but just for precautions
    for i in range(len(nbc_article_info)):
        if 'video' in nbc_article_info[i]['url']:
            nbc_article_info[i].clear()
        elif 'watch' in nbc_article_info[i]['url']:
            nbc_article_info[i].clear()
        elif '?' in nbc_article_info[i]['url']:
            nbc_article_info[i].clear()
        elif 'Live updates' in nbc_article_info[i]['headline']:
            nbc_article_info[i].clear()
    #remove empty dictionaries left from cleaning article link data
    while {} in nbc_article_info:
        nbc_article_info.remove({})

def nbcArticleTextScraper(url):
    article_page = requests.get(url)
    article_soup = BeautifulSoup(article_page.text, 'lxml')
    article_text = article_soup.find('div', class_='article-body__content').get_text()
    return article_text

scrapeNbcSite()