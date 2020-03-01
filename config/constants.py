import os

CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET_KEY")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_SECRET_KEY")
TARGET_NAME = os.getenv("TWITTER_TARGET")
DATABASE_NAME = 'tweetkov'
TWEET_COLLECTION_NAME = 'tweets'
CHAIN_COLLECTION_NAME = 'chains'
MONGO_URL = 'mongodb://localhost:27017'
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")