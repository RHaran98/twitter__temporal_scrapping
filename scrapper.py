import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
import datetime,tweepy
from timex import tag

credentials = {}

today = datetime.datetime.now()
date_limit = today - datetime.timedelta(days=0)


class TwitterHandler:
    def __init__(self):
        self.credentials = {}
        self.credentials['CONSUMER_KEY'] = ''       # Enter consumer key here
        self.credentials['CONSUMER_SECRET'] = ''    # Enter consumer secret here
        self.credentials['ACCESS_TOKEN'] = ''       # Enter access token here
        self.credentials['ACCESS_SECRET'] = ''      # Enter access secret here
        self.today = datetime.datetime.now()
        self.auth = OAuthHandler(self.credentials['CONSUMER_KEY'], self.credentials['CONSUMER_SECRET'])
        self.auth.set_access_token(self.credentials['ACCESS_TOKEN'], self.credentials['ACCESS_SECRET'])
        self.api = API(self.auth)

    def getTweets(self,date,max_tweets,topic):
        '''

        :param date: python datetime object
        :param max_tweets: Maximum number of tweets to return
        :param topic: Topic to search from
        :return: List of tuples, tuple format (date,tweet)
        '''
        from_date = date -datetime.timedelta(days=1)
        from_date = from_date.strftime("%Y-%m-%d")
        to_date = date + datetime.timedelta(days=1)
        to_date = to_date.strftime("%Y-%m-%d")
        tweets = []
        for tweet in tweepy.Cursor(self.api.search, q=topic + ' -filter:retweets', since=from_date, until=to_date).items(max_tweets):
            tweet_date = tweet._json['created_at']
            tweet_text = tweet._json['text']
            tweets.append((tweet_date,tweet_text))
        return tweets

    def getTimelineTweets(self,date,max_tweets,topic):
        '''

        :param date: python datetime object
        :param max_tweets: Maximum number of tweets to return
        :param topic: Topic to search from
        :return: List of tuples, tuple format (date,tweet)
        '''
        from_date = date -datetime.timedelta(days=1)
        from_date = from_date.strftime("%Y-%m-%d")
        to_date = date + datetime.timedelta(days=1)
        to_date = to_date.strftime("%Y-%m-%d")
        curr_tweets = 0
        tweets = []
        for tweet in tweepy.Cursor(self.api.search, q=topic + ' -filter:retweets', since=from_date, until=to_date).items():
            tweet_date = tweet._json['created_at']
            tweet_text = tweet._json['text']
            if len(tag(tweet_text)) > len(tweet_text):  # Filter out non timeline sentences
                tweets.append((tweet_date,tweet_text))
                curr_tweets += 1
            if curr_tweets >= max_tweets:
                break
        return tweets



if __name__ == '__main__':
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
    for tweet in tweepy.Cursor(api.search, q=query,lang=['en'],since=from_date,until=to_date).items():
        for i in range(1,4):
            tweet_date = datetime.datetime.strptime(tweet._json['created_at'],"%a %b %d  %H:%M:%S %z %Y")
            if tweet_date.date() == (today - datetime.timedelta(days=i)).date():
                tweets['{0}daysago'.format(i)].append((tweet._json['text'],tweet._json['created_at']))
                curr_tweets +=1
                if curr_tweets >= max_tweets:
                    break
        if curr_tweets >= max_tweets:
            print("Done")
            break
    print(tweets)