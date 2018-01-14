from flask import Flask, render_template
from flask_socketio import SocketIO
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import global_const as const
from textblob import TextBlob
import json
import eventlet
eventlet.monkey_patch()

# Variables that contains the user credentials to access Twitter API
access_token = const.access_token
access_token_secret = const.access_token_secret
consumer_key = const.consumer_key
consumer_secret = const.consumer_secret

app = Flask(__name__)
sio = SocketIO(app)


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
        resp = {"text": tweet['text'], "userId": tweet['user']['name'], "userName": tweet['user']['screen_name'],
                "sentiment": polarity, "subjectivity": subjectivity}
        if const.Debug:
            print('Status: Sending New Tweet')
        sio.emit("notification", {"tweet": resp})
        # print rep

    def on_error(self, status):
        print status


def start_stream():
    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = Listener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=const.filter_keywords)

    if const.Debug:
        print('Status: Stream Instance Created.')


@app.route("/")
def index():
    return render_template('index.html')


@sio.on("fire_start")
def on_start(data):
    if const.Debug:
        print('Fire Service Request: {0}'.format(str(data)))
        start_stream()


@sio.on('client_connected')
def handle_client_connect_event(data):
    print('received json: {0}'.format(str(data)))
    sio.emit('connection_accepted', data)


if __name__ == "__main__":
    app.debug = False
    sio.run(app, port=5000, debug=False, use_reloader=True)
    # sio.run(app, port=5000)
