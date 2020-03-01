import tweepy
import config.constants


class TwitterAccess(object):
    def __init__(self):
        self._consumer_key = config.constants.CONSUMER_KEY
        self._consumer_secret = config.constants.CONSUMER_SECRET
        self._access_token = config.constants.ACCESS_TOKEN
        self._access_token_secret = config.constants.ACCESS_TOKEN_SECRET

    def retrieve_all_tweets(self, user_name):
        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)
        api = tweepy.API(auth)

        all_tweets = []

        last_tweets = api.user_timeline(screen_name=user_name, count=200)
        all_tweets.extend(last_tweets)

        oldest = all_tweets[-1].id - 1

        while len(last_tweets) > 0:
            last_tweets = api.user_timeline(screen_name=user_name, count=200, max_id=oldest)
            all_tweets.extend(last_tweets)
            oldest = all_tweets[-1].id - 1

        return all_tweets

    def retrieve_tweets_since_id(self, user_name, id):
        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)
        api = tweepy.API(auth)

        return api.user_timeline(screen_name=user_name, since_id=id)

    def send_tweet(self, user_name, tweetkov_tweet):
        auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        auth.set_access_token(self._access_token, self._access_token_secret)
        api = tweepy.API(auth)
        last_tweet = api.user_timeline(screen_name=user_name, count=1)
        for tweet in last_tweet:
            entire_tweet = "@{} {}".format(user_name, tweetkov_tweet)
            api.update_status(entire_tweet, in_reply_to_status_id = tweet.id)
