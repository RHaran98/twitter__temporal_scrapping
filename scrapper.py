import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
import datetime,tweepy

credentials = {}
credentials['CONSUMER_KEY'] = 'yfnS1Fqzh4EBnqrKXs0C9fnls'
credentials['CONSUMER_SECRET'] = 'CDX1TDnzQLMuOezhAxLmSerirZLXhAaJuAALxZ4PDtanSn4sT7'
credentials['ACCESS_TOKEN'] = '2811020677-cygjhFFFyEGhUATHsD1iAbtcP493qZWSO7lYJ8P'
credentials['ACCESS_SECRET'] = 'BghXsGvcPhkUdlpUsNmjUNZiHE6prPgzlfWVO7D45pM5e'
today = datetime.datetime.now()
date_limit = today - datetime.timedelta(days=0)

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print (status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
    auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    api = API(auth)
    query = 'a' # input("Enter topic to search on twitter : ")
    max_tweets = 10
    curr_tweets = 0
    from_date = today - datetime.timedelta(days=5)
    from_date = from_date.strftime("%Y-%m-%d")
    to_date = today - datetime.timedelta(days=0)
    to_date = to_date.strftime("%Y-%m-%d")
    tweets = {"1daysago":[],"2daysago":[],"3daysago":[]}
    for tweet in tweepy.Cursor(api.search, q=query,since=from_date,until=to_date).items():
        for i in range(1,4):
            tweet_date = datetime.datetime.strptime(tweet._json['created_at'],"%a %b %d  %H:%M:%S %z %Y")
            if tweet_date.date() == (today - datetime.timedelta(days=i)).date():
                print(tweet_date.date())
                tweets['{0}daysago'.format(i)].append((tweet._json['text'],tweet._json['created_at']))
                print(tweet._json['text'],tweet._json['created_at'])
                curr_tweets +=1
                if curr_tweets >= max_tweets:
                    break
        if curr_tweets >= max_tweets:
            print("Done")
            break
    print(tweets)