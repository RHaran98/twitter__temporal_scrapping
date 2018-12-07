from scrapper import TwitterHandler
import datetime
from rake_nltk import Rake


r = Rake()
t = TwitterHandler()

today = datetime.datetime.now()
tweets = t.getTimelineTweets(today,10,"#MeToo")
concat = ''
for time,tweet in tweets:
    r.extract_keywords_from_text(tweet)
    events = r.get_ranked_phrases()
    topic = events[0]
    print("Topics : ",topic)
    print(tweet)
    print("Events : ",events)
    print("\n\n")
