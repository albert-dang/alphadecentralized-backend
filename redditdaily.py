#Scrape Reddit for the most mentioned tickers

import praw
import re
import pandas as pd
from datetime import datetime as dt

#Read in and return a list of top tickers from the previous execution
def get_prev_tickers():
    prev = open('prev.txt', 'r')
    prevTickers = prev.readlines()
    prev.close()
    return prevTickers

#Read in CSVs and return a dictionary of tickers
def get_stocklist():
    tickerDict = {}
    fileList = ['list1.csv', 'list2.csv', 'list3.csv']
    for file in fileList:
        tickerList = pd.read_csv(file, skiprows=0, skip_blank_lines=True)
        tickerList = tickerList[tickerList.columns[0]].tolist()

        for ticker in tickerList:
            tickerDict[ticker] = 1
    return tickerDict


def get_tickers(sub, stockList):
    reddit = praw.Reddit(client_id='CLIENT ID', \
                         client_secret='SECRET KEY', \
                         user_agent='USER AGENT', \
                         username='USERNAME', \
                         password='PASSWORD')

    dailyTickers = {}
    regexPattern = r'\b([A-Z]+)\b'
    tickerDict = stockList
    blacklist = ['A', 'I', 'DD', 'WSB', 'YOLO', 'RH', 'EV', 'PE', 'ETH', 'BTC', 'E']
    for thread in reddit.subreddit(sub).top('day'):
        strings = [thread.title]
        thread.comments.replace_more(limit=0)
        for comment in thread.comments.list():
            strings.append(comment.body)
        for s in strings:
            for phrase in re.findall(regexPattern, s):
                if phrase not in blacklist:
                    if phrase in tickerDict:
                        if phrase not in dailyTickers:
                            dailyTickers[phrase] = 1
                        else:
                            dailyTickers[phrase] += 1
    return dailyTickers

prevTickers = get_prev_tickers()
subs = ['wallstreetbets', 'wallstreetbetsnew', 'stocks', 'investing', 'smallstreetbets']
stockList = get_stocklist()
topTickers = {}
for sub in subs:
    dailyTickers = get_tickers(sub, stockList)
    for ticker in dailyTickers.keys():
        if ticker in topTickers:
            topTickers[ticker] += dailyTickers[ticker]
        else:
            topTickers[ticker] = dailyTickers[ticker]

#Log the data
with open('mydir/stockslog.csv','a') as file:
    #Get the current datetime object
    now = dt.now()
    #Parse datetime into string
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    for ticker in topTickers:
        file.write(now + ',' + ticker + ',' + str(topTickers[ticker]) + '\n')

top10 = sorted(topTickers, key=topTickers.get, reverse=True)[:10]
with open('mydir/topstocks.csv','w') as file:
    file.write('ticker,mentions\n')
    for top in top10:
        file.write(top + ',' + str(topTickers[top]) + '\n')
