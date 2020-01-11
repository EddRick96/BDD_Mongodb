from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient

MONGO_HOST= 'mongodb+srv://Erick:Admin123@cluster0-yndgh.gcp.mongodb.net/test?retryWrites=true&w=majority'  # assuming you have mongoDB installed locally
                                             # and a database called 'twitterdb'

WORDS = ['#bigdata', '#AI', '#datascience', '#machinelearning', '#ml', '#iot']

CONSUMER_KEY = 'cVZzG24tkXeYelkgZVKdOqPVZ'
CONSUMER_SECRET = 'm68V2cjhwrzmWNGWqg5eUb0TmZKpUhHrYtHIMYliHel3COOiED'
ACCESS_TOKEN = '1199829431814148097-QqfF1LbU5bM6KtxfhpGjH05pN8moZN'
ACCESS_TOKEN_SECRET = '4oqyvwiQg2CssTlFE8i29Q1bgjGHnJAeIJ0azpVsdpg8Z'

class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            client = MongoClient(MONGO_HOST)
            
            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.bdd
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            
            #grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']

            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))
            
            #insert the data into the mongoDB into a collection called twitter_search
            #if twitter_search doesn't exist, it will be created.
            db.testuno.insert(datajson)
        except Exception as e:
           print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)
