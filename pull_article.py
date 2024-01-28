import requests
from sentiment_analyis.pymongo_get_database import get_database
from sentiment_analyis.embed import get_embedding
from datetime import datetime
#All news article scraping and maintainance goes here

Vectors = get_database()
articles = Vectors["table"]

#convert unix timestamp to date format YYMMDDTHHMM
def unix_to_time(unix_date):
    return datetime.utcfromtimestamp(unix_date).strftime('%Y%m%dT%H%M')

#convert date in fortmat YYMMDDTHHMM to unix timestamp
def time_to_unix(date):
    return datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), int(date[9:11]), int(date[11:13])).timestamp()

#pull article headlines about asset from alpha-vantage, limited to date range in format YYYYMMDDTHHMM
#embed article summary with openAI embeddings
#append result to MongoDB 'articles' database, with no duplicates in article url
def pull_AV_articles(limit,asset,dates):
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&sort=RELEVANCE&tickers=' + asset + '&limit=' + str(limit) + '&time_from=' + dates[0] + '&time_to=' + dates[1] + '&apikey=YOURAPIKEY'
    r = requests.get(url)
    data = r.json()
    prep = []
    for item in data['feed']:
        #avoid repeat articles, and empty summaries
        if list(articles.find({'link': item['url']})) == [] and len(item['summary']) > 10:
            prep.append({'link': item['url'],
                    'date': time_to_unix(item['time_published']),
                    'vector': get_embedding(item['summary'])})
    #get number of articles added, and an example summary
    print(str(len(prep)) + ' articles added')
    print(data['feed'][0]['summary'])
    articles.insert_many(prep)

#add up to 1000 articles per quarter about asset, for a year
def aggregate_yearly_articles(start):
    seconds_in_quarter = 60*60*24*90
    for i in range(4):
        pull_AV_articles(1000, 'CRYPTO:BTC', [unix_to_time(start),unix_to_time(start + seconds_in_quarter)])
        start += seconds_in_day

#aggregate_yearly_articles(time_to_unix('20230101T0000'))
