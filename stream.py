from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import global_const as const

# Variables that contains the user credentials to access Twitter API
access_token = const.access_token
access_token_secret = const.access_token_secret
consumer_key = const.consumer_key
consumer_secret = const.consumer_secret


# listener
class Listener(StreamListener):

    def on_data(self, data):
        print data
        return True

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
