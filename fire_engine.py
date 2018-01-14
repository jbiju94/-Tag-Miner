from flask import Flask, render_template
from flask_socketio import SocketIO
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import global_const as const
from textblob import TextBlob
import json
import math
import eventlet
eventlet.monkey_patch()

# Variables that contains the user credentials to access Twitter API
access_token = const.access_token
access_token_secret = const.access_token_secret
consumer_key = const.consumer_key
consumer_secret = const.consumer_secret

app = Flask(__name__)
sio = SocketIO(app)

keyword_params = ""


# listener
class Listener(StreamListener):
    tweet_total_count = 0
    tweet_positive_count = 0
    tweet_negative_count = 0
    tweet_neutral_count = 0

    def on_data(self, data):
        tweet = json.loads(data)
        if tweet['retweeted']:
            return

        Listener.tweet_total_count += 1

        blob = TextBlob(tweet['text'])
        sent = blob.sentiment

        polarity = sent.polarity
        subjectivity = sent.subjectivity

        if polarity < 0:
            Listener.tweet_negative_count += 1
        elif polarity == 0:
            Listener.tweet_neutral_count += 1
        else:
            Listener.tweet_positive_count += 1

        resp = {"text": tweet['text'], "userId": tweet['user']['screen_name'], "userName": tweet['user']['name'],
                "userImage": tweet['user']['profile_image_url_https'],
                "tweetTime": tweet['created_at'], "sentiment": polarity, "subjectivity": subjectivity}

        count = {"total": Listener.tweet_total_count,
                 "positive": Listener.tweet_positive_count,
                 "positive_percent": math.floor((Listener.tweet_positive_count / Listener.tweet_total_count)),
                 "neutral":  Listener.tweet_neutral_count,
                 "neutral_percent": math.floor((Listener.tweet_neutral_count / Listener.tweet_total_count)),
                 "negative": Listener.tweet_negative_count,
                 "negative_percent": math.floor((Listener.tweet_negative_count / Listener.tweet_total_count))
                 }

        if const.Debug:
            print('Status: Sending New Tweet')
        sio.emit("notification", {"tweet": resp, "count": count})
        # print rep

    def on_error(self, status):
        print status


def start_stream(data):
    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = Listener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    if not data:
        # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
        stream.filter(track=const.filter_keywords)
    else:
        stream.filter(track=data.split(","))

    if const.Debug:
        print('Status: Stream Instance Created.')


@app.route("/")
def index():
    return render_template('index.html')


@sio.on("fire_start")
def on_start(data):
    if const.Debug:
        print('Fire Service Request: {0}'.format(str(data)))
        start_stream(data['data'])


@sio.on('client_connected')
def handle_client_connect_event(data):
    print('received json: {0}'.format(str(data)))
    sio.emit('connection_accepted', data)


if __name__ == "__main__":
    app.debug = False
    sio.run(app, port=5000, debug=False, use_reloader=True)
    # sio.run(app, port=5000)
