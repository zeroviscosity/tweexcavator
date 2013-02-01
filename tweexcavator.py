#!/usr/bin/env python

import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
from tweepy.api import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class Tweexcavator(StreamListener):
    """Overrides tweepy's StreamListener class in order to add a database
    connection and save incoming tweets."""
    
    def establish_db_connection(self, host, name, collection):
        """Used to establish the connection to MongoDB and open the requested
        connection."""
        
        try:
            connection = MongoClient(host)
            db = connection[name]
            self.collection = db[collection]
            print "Successfully connected to database"            
        except ConnectionFailure, e:
            sys.stderr.write("Failed to connect to MongoDB: %s\n" % e)
            sys.exit(1)

    def on_status(self, status):
        """Overrides the on_status method of tweepy's StreamListener in order 
        to save tweet data in the database collection."""
      
        tweet = { "id": status.id,
                  "text": status.text,
                  "created_at": status.created_at,
                  "author": {
                    "name": status.author.name,
                    "screen_name": status.author.screen_name } }
        try:
            self.collection.insert(tweet)
            print "Successfully saved tweet %d" % status.id
        except OperationFailure, e:
            sys.stderr.write("Failed to save tweet %d: %s\n" % (status.id, e))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.stderr.write(
            "Invalid number of arguments. Usage:\n"
            "tweexcavator.py db_host db_name db_collection\n"
        )
        sys.exit(1)
    else:
        #Obtain the following from https://dev.twitter.com/
        consumer_key = ""
        consumer_secret = ""
        access_token = ""
        access_token_secret = ""
        
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        listener = Tweexcavator()
        listener.establish_db_connection(sys.argv[1], sys.argv[2], sys.argv[3])
        
        streamer = Stream(auth, listener)
        streamer.sample()
