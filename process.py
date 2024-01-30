import time
import numpy as np
from sentiment_analyis.pymongo_get_database import get_database
from sentiment_analyis.pymongo_db import query,migrate
from sentiment_analyis.pull_article import time_to_unix
from sentiment_analyis.embed import get_embedding
import yfinance as yf


Vectors = get_database()
articles = Vectors["table"]
validation_articles = Vectors["validation_table"]

#compute how many days ago a unix timestamp is
def days_ago(timestamp):
    return int((time.time() - timestamp)/(60*60*24))

#use yahoo finance api to get daily BTC opening price
BTC_Ticker = yf.Ticker("BTC-USD")
BTC_Data = BTC_Ticker.history(period="max")
data = [list(BTC_Data.iloc[i][0:5]) for i in range(len(BTC_Data))]

#Compute the mean change in price for the next week, as a ratio of current price
def compute_weekly_performance(unix_date):
    daysAgo = days_ago(unix_date)
    prices = [i[0] for i in data[-daysAgo - 1: -daysAgo + 6]]
    return (np.mean(prices) - prices[0])/prices[0]

#compute performance metrics associated to articles in the articles database
def update_classes():
    table = articles.find()
    for item in list(table):
        result = compute_weekly_performance(item['date'])
        articles.update_one({'_id': item['_id']},{'$set': { 'class': result  } })

def predict(article, k, candidates):
    # total measure of articles published when asset moves at least 1% that week
    positive_articles = articles.count_documents({'class': {'$gt': 0.01}})
    negative_articles = articles.count_documents({}) - positive_articles
    weight_neg = negative_articles / (negative_articles + positive_articles)
    weight_pos = positive_articles / (negative_articles + positive_articles)
    neighbours = query(get_embedding(article), k, candidates)
    good_neighbours = sum([1 for a in list(neighbours) if a['class'] > 0.01])
    # we need to weight the sample accoridng to total articles
    probability = (good_neighbours / weight_pos) / (good_neighbours / weight_pos + (k - good_neighbours) / weight_neg)
    return probability

#check performance of articles by using validation_articles
#k nearest neighbours, candidates is typically 20*k
def validate(k,candidates):
    #total measure of articles published when asset moves at least 1% that week
    positive_articles = articles.count_documents({'class':{'$gt':0.01}})
    negative_articles = articles.count_documents({}) - positive_articles
    weight_neg = negative_articles/ (negative_articles + positive_articles)
    weight_pos = positive_articles/ (negative_articles + positive_articles)
    table = validation_articles.find()
    errors = 0
    total = 0
    print('The proportion of articles influencing BTC to move >1% is ' + str(weight_pos))
    for item in table:
        neighbours = query(item['vector'],k,candidates)
        good_neighbours = sum([1 for a in list(neighbours) if a['class'] > 0.01])
        #we need to weight the sample accoridng to total articles
        probability = (good_neighbours / weight_pos) / (good_neighbours / weight_pos + (k - good_neighbours) / weight_neg)
        #only execute if sure
        if probability < 0.8:
            continue
        total += 1
        #count errors, if BTC actually moves negatively
        if item['class'] < 0:
            errors += 1
        print('I am ' + str(probability) + ' sure that BTC will go up, but the actual performance is ' + str(item['class']))
        print('cumulative error: ' + str(errors/total))

#validate(24,500)
