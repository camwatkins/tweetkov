from pymongo import MongoClient
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError, WriteError
from config.constants import TWEET_COLLECTION_NAME
from config.constants import CHAIN_COLLECTION_NAME
import time


class MongoAccess(object):
    def __init__(self, url, db):
        try:
            self._client = MongoClient(url, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
            self._client.server_info()
            self._database = self._client[db]
        except ServerSelectionTimeoutError:
            raise ConnectionError
        except OperationFailure as err:
            raise ConnectionError

    def check_for_existing_entries(self, status):
        tweet_collection = self._database[TWEET_COLLECTION_NAME]
        document = tweet_collection.find({
            "id": status.id
        })
        return len(list(document)) > 0

    def get_last_entry_id(self):
        tweet_collection = self._database[TWEET_COLLECTION_NAME]
        document = tweet_collection.find().sort("id", 1).limit(1)
        entry = list(document)
        if entry:
            return entry[0].get("id")
        else:
            return None

    def insert_status_into_mongo(self, status):
        tweet_collection = self._database[TWEET_COLLECTION_NAME]
        return tweet_collection.insert_one(status.as_dict()).inserted_id

    def find_chain_by_value(self, value):
        chain_collection = self._database[CHAIN_COLLECTION_NAME]
        document = chain_collection.find({
            "value": value
        })
        return list(document)

    def insert_chain_into_mongo(self, chain_value, link_value):
        chain_collection = self._database[CHAIN_COLLECTION_NAME]
        chain_collection.insert_one({
            "value": chain_value,
            "links": [{"value": link_value, "count": 1}]
        })

    def update_chain_in_mongo(self, entry, link_value):
        chain_collection = self._database[CHAIN_COLLECTION_NAME]
        exists = False
        for link in entry.get("links"):
            if link.get("value") == link_value:
                exists = True

        if exists:
            chain_collection.update_one({
                "_id": entry.get("_id"),
                "links.value": link_value
            }, {
                "$inc":
                    {
                        "links.$.count": 1
                    }
            }
            )
        else:
            chain_collection.update_one({
                "_id": entry.get("_id"),
            }, {
                "$push": {
                    "links": {"value": link_value, "count": 1}
                }}
            )

    def create_chain_from_existing_tweets(self):
        tweet_collection = self._database[TWEET_COLLECTION_NAME]
        cursor = tweet_collection.find({})

        for tweet in cursor:
            self.create_chain_from_single_tweet(tweet.get("text"))

    def create_chain_from_single_tweet(self, tweet):
        words = tweet.split()

        # Look up each word in the chain database.
        i = 0
        while i < (len(words) - 2):
            # Look up the current word in the database.
            current = self._strip_dot_dot_dot(words[i])
            next = self._strip_dot_dot_dot(words[i + 1])
            existing = self.find_chain_by_value(words[i])
            # There is an existing entry.
            if len(existing) == 0:
                self.insert_chain_into_mongo(current, next)
            else:
                self.update_chain_in_mongo(existing[0], next)
            time.sleep(.01)
            i = i + 1

    def get_random_tweet_text(self):
        tweet_collection = self._database[TWEET_COLLECTION_NAME]
        cursor = tweet_collection.aggregate([{"$sample": {"size": 1}}])
        for tweet in cursor:
            if tweet.get("text"):
                return tweet.get("text")
            else:
                return None

    def _strip_dot_dot_dot(self, word):
        encoded = word.encode("utf-8")
        if encoded.endswith(b"\xe2\x80\xa6"):
            return encoded[:-3].decode("utf-8")
        if encoded.startswith(b"\xe2\x80\xa6"):
            return encoded[3:].decode("utf-8")
        return encoded.decode("utf-8")
