#Scrape Reddit for the most mentioned tickers

import praw
import re
import pandas as pd
from datetime import datetime as dt

#Read in CSVs and return a dictionary of tickers
def get_stocklist():
    #Dictionary for storing tickers and counts
    tickerDict = {}
    #Your CSVs for storing tickers to scan
    fileList = ['list1.csv', 'list2.csv', 'list3.csv']
    #For each CSV
    for file in fileList:
        #Read the CSV into a Pandas DataFrame
        tickerList = pd.read_csv(file, skiprows=0, skip_blank_lines=True)
        #Transform the DataFrame into a list
        tickerList = tickerList[tickerList.columns[0]].tolist()
        #For each ticker in the list
        for ticker in tickerList:
            #Populate the dictionary of tickers with a count of 0
            tickerDict[ticker] = 0
    return tickerDict

#Use the Reddit API to count mentions
def get_tickers(sub, tickerDict):
    #The following link points to the sign up form for a Reddit API key:
    #https://docs.google.com/forms/d/e/1FAIpQLSezNdDNK1-P8mspSbmtC2r86Ee9ZRbC66u929cG2GX0T9UMyw/viewform
    reddit = praw.Reddit(client_id='CLIENT ID', \
                         client_secret='SECRET KEY', \
                         user_agent='USER AGENT', \
                         username='USERNAME', \
                         password='PASSWORD')
    #Dictionary for storing tickers and mention counts
    dailyTickers = {}
    #Regular expression pattern for matching mentions
    regexPattern = r'\b([A-Z]+)\b'
    #Blacklist certain tickers, tags or symbols which are confusing, i.e. shared with crypto 
    blacklist = ['A', 'I', 'DD', 'WSB', 'YOLO', 'RH', 'EV', 'PE', 'ETH', 'BTC', 'E']
    #For each thread in the subreddit, sorted by top today
    for thread in reddit.subreddit(sub).top('day'):
        #Get the thread title
        strings = [thread.title]
        #Do not look at comments beyond "show more"
        thread.comments.replace_more(limit=0)
        #For each comment in the thread
        for comment in thread.comments.list():
            #Append the commen
            strings.append(comment.body)
        #For each character in the string
        for s in strings:
            #Find matches
            for phrase in re.findall(regexPattern, s):
                #Check if the ticker has been blacklisted
                if phrase not in blacklist:
                    if phrase in tickerDict:
                        #Check if the ticker has already been recorded
                        if phrase not in dailyTickers:
                            #If not, create the key and set its count to 1
                            dailyTickers[phrase] = 1
                        else:
                            #If the key exists, increment the count
                            dailyTickers[phrase] += 1
    return dailyTickers

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
with open('stockslog.csv','a') as file:
    #Get the current datetime object
    now = dt.now()
    #Parse datetime into string
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    for ticker in topTickers:
        file.write(now + ',' + ticker + ',' + str(topTickers[ticker]) + '\n')

top10 = sorted(topTickers, key=topTickers.get, reverse=True)[:10]
with open('topstocks.csv','w') as file:
    file.write('ticker,mentions\n')
    for top in top10:
        file.write(top + ',' + str(topTickers[top]) + '\n')
