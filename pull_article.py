import requests
from sentiment_analyis.pymongo_get_database import get_database
from sentiment_analyis.embed import get_embedding
from datetime import datetime
#All news article scraping and maintainance goes here

Vectors = get_database()

#convert unix timestamp to date format YYMMDDTHHMM
def unix_to_time(unix_date):
    return datetime.utcfromtimestamp(unix_date).strftime('%Y%m%dT%H%M')

#convert date in fortmat YYMMDDTHHMM to unix timestamp
def time_to_unix(date):
    return datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), int(date[9:11]), int(date[11:13])).timestamp()

f = open("article.txt", encoding='utf8')
text = " ".join(f.read().split())

#add one article to curated table for asset
def add_article(asset,url,text,date,label = None, source = None):
    table = Vectors['Assets']
    #no duplicates in url
    if list(table.find({'link': url })) == []:
        table.insert_one({'asset': asset, 'link': url, 'source': source,
                     'date': time_to_unix(date),
                     'vector': get_embedding(text),'label' : label})

