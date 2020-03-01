from lib.data.mongo_access import MongoAccess
from lib.data.twitter_access import TwitterAccess
from lib.classes.status import Status
from lib.classes.tweetkov import Tweetkov
import config.constants
import logs
import logging
import discord
from lib.classes.voting_booth import VotingBooth
import time
import asyncio


def build_chains(mongo):
    mongo.create_chain_from_existing_tweets()


def main():
    mongo = None
    twitter = TwitterAccess()
    tweetkov = Tweetkov()
    logger = logging.getLogger(__name__)
    tweet_count = 0
    voting_booth = VotingBooth()
    voting_results = []

    client = discord.Client()

    try:
        logger.info("Attempting to connect to MongoDB...")
        mongo = MongoAccess(config.constants.MONGO_URL, config.constants.DATABASE_NAME)
        logger.info("Successfully connected to MongoDB!")
    except ConnectionError:
        logger.warning("Could not connect to MongoDB!")
        exit()

    last_tweet_id = mongo.get_last_entry_id()

    if last_tweet_id:
        logger.info("Found old tweets! Fetch starting from id: {}".format(str(last_tweet_id)))
        all_tweets = twitter.retrieve_tweets_since_id(config.constants.TARGET_NAME, last_tweet_id)
    else:
        all_tweets = twitter.retrieve_all_tweets(config.constants.TARGET_NAME)
        logger.info('Total tweets found: {}'.format(str(len(all_tweets))) + str(len(all_tweets)))

    for tweet in all_tweets:
        full_tweet = Status(tweet)
        if not mongo.check_for_existing_entries(full_tweet):
            logger.debug("** Inserting: {} into database! ".format(str(full_tweet.id)))
            mongo.insert_status_into_mongo(full_tweet)
            mongo.create_chain_from_single_tweet(full_tweet.text)
            tweet_count = tweet_count + 1
    if tweet_count == 0:
        logger.info("No new tweets added!")
    else:
        logger.info("Total tweets added: {}".format(str(tweet_count)))

    def get_chains(quantity):
        chains = []
        for index in range(quantity):
            chains.append(tweetkov.build_that_chain(mongo))
        return chains

    @client.event
    async def on_ready():
        await client.change_presence(game=discord.Game(name="with your political emotions..."))

    @client.event
    async def on_message(message):
        if message.author != client.user:
            if message.content[0] == "!":
                if voting_booth.is_voting():
                    try:
                        voting_booth.vote(int(message.content[1]))
                    except ValueError:
                        return
                elif message.content == "!build":
                    logger.info("Generating Tweetkov chain...")
                    chains = get_chains(1)
                    for index, chain in enumerate(chains, start=0):
                        await client.send_message(message.channel, "{}: {}".format(index, chain))
                elif message.content == "!vote":
                    await client.send_message(message.channel, "Voting begins...")
                    logger.info("Generating Tweetkov chain...")
                    chains = get_chains(5)
                    for index, chain in enumerate(chains, start=0):
                        time.sleep(1)
                        await client.send_message(message.channel, "[!{}]: {}".format(index, chain))
                    voting_booth.start_voting(chains, 10)
                    while voting_booth.is_voting():
                        time.sleep(1)
                        await asyncio.sleep(10)  # task runs every 60 seconds
                        await client.send_message(message.channel, "Winner: {}".format(voting_booth.results()))
                        voting_booth.stop_voting()

    client.run(config.constants.DISCORD_TOKEN)

    # logger.info("Generating Tweetkov chain...")
    # new_tweet = tweetkov.build_that_chain(mongo)
    #
    # logger.info("Tweeting chain: {}".format(new_tweet))
    # twitter.send_tweet(config.constants.TARGET_NAME, new_tweet)


if __name__ == "__main__":
    logs.configure_logging()
    main()