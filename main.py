from scrapper import TwitterHandler
import datetime
from rake_nltk import Rake


r = Rake()
t = TwitterHandler()

today = datetime.datetime.now()
query = input("Enter topic to search for : ")
max_tweets = input("Number of tweets to retrieve per day : ")

tweets = []
for i in range(1,4):    # Last three days
    tweets.extend(t.getTimelineTweets(today-datetime.timedelta(days=i),max_tweets,query))

for time,tweet in tweets:
    r.extract_keywords_from_text(tweet)
    events = r.get_ranked_phrases()
    topic = events[0]
    print("Topics : ",topic)
    print(tweet)
    print("Events : ",events)
    print("\n\n")
