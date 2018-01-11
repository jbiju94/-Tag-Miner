from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import global_const as const
import json
from textblob import TextBlob

# Variables that contains the user credentials to access Twitter API
access_token = const.access_token
access_token_secret = const.access_token_secret
consumer_key = const.consumer_key
consumer_secret = const.consumer_secret


# listener
class Listener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        if tweet['retweeted']:
            return

        blob = TextBlob(tweet['text'])
        sent = blob.sentiment

        polarity = sent.polarity
        subjectivity = sent.subjectivity

        positive_sentiment = True
        if polarity < 0:
            positive_sentiment = False

        tweet['positive_sentiment'] = positive_sentiment
        print {"text": tweet['text'], "userId": tweet['user']['name'], "userName": tweet['user']['screen_name'],
               "positiveSentiment": tweet['positive_sentiment']}

    def on_error(self, status):
        print status


if __name__ == '__main__':

    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = Listener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
