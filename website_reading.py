from bs4 import BeautifulSoup
import requests
import json


def title(site_url):
    """
    If possible, returns a title of the website, else just returns the website address.
    """
    try:
        html_site = requests.get(site_url, verify=False).text
        soup = BeautifulSoup(html_site, 'lxml')
        title = soup.head.title.text
    except:
        title = site_url
    return title

def readArticle(link):
    """
    Reads the article at the given website address and returns a tuple with two values: 
    heading and text of the article.
    """
    html_article = requests.get(link, verify=False).text
    soup = BeautifulSoup(html_article, 'lxml')
    heading = soup.article.header.text
    content = soup.article.find('div', class_='entry-content clr').text
    return (heading, content)

def getArticles(site_url='https://polito.uz/news/'):
    """
    Reads all existing articles from the given website.
    Returns a dictionary with links to the articles as keys and return values from readArticle() function as values.
    Saves the dictionary into the file 'Articles.json'.
    """
    html_text = requests.get(site_url, verify=False).text
    soup = BeautifulSoup(html_text, 'lxml')
    articles = {}
    articles_list = soup.find_all('article')
    for article in articles_list:
        articleLink = article.h2.a['href']
        articleContent = readArticle(articleLink)
        articles[articleLink] = articleContent
    json.dump(articles, open('Articles.json','w'), indent=4, separators=(', ',' : '))
    return articles



