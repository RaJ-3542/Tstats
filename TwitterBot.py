import tweepy
import configparser
import pandas as panda
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
analysis = SentimentIntensityAnalyzer()          

config = configparser.ConfigParser()
config.read('config.ini')


api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']
auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

def fetch(words):
    db = panda.DataFrame(columns=['tweet'])
    tweets = tweepy.Cursor(api.search_tweets,
                               words, lang="en",
                               tweet_mode='extended').items(100)
    list_tweets = [tweet for tweet in tweets]
    tweetsWithSent = []
    p = 0
    q = 0
    n = 0
    maax = -1.0
    minn = sys.maxsize

    for tweet in list_tweets:
            try:
                    text = tweet.retweeted_status.full_text
                    res = analysis.polarity_scores(text)
                    if res['compound']>0.0:
                        p+=1
                        maax = max(maax,res['compound'])
                        if maax==res['compound']:
                            positiveTweets = text
                    elif res['compound']<0.0:
                        q+=1
                        minn = min(minn,res['compound'])
                        if minn == res['compound']:
                            negativeTweets = text
                    else:
                        n+=1
                    tweetsWithSent.append({'text':text,'compound':res['compound']})
            except AttributeError:
                    text = tweet.full_text
    p = p/(p+q+n)*100
    q = q/(p+q+n)*100
    n = n/(p+q+n)*100
    # print(round(float(p),2))
    # print("\n",round(float(q), 2))
    
    # print("\n",round(float(n), 2))

    listStats = [round(float(p),2),round(float(q), 2),round(float(n), 2),positiveTweets,negativeTweets]

    # print(positiveTweets)
    # print("\n oneee")
    # print("\n",negativeTweets)
    



    # print("\nPositive Tweets : ",p,end=" %")
    # print("\nNegative Tweets : ",q,end=" %")
    # print("\nNeutral Tweets : ",n,end=" %")
    
    filename = 'scraped_tweets.csv'
    db.to_csv(filename)

    return listStats

# if __name__ == '__main__':
#     print('Enter twitter # : ')
#     words = input()

#     fetch(words)











