import lib.classes.chain_tools


class Tweetkov(object):
    def build_that_chain(self, mongo_connector):
        chain = self._random_tweet_seed(mongo_connector)
        next_word = chain
        while (chain.endswith(".") or chain.endswith("!") or chain.endswith("?")) is not True:
            chain_piece = mongo_connector.find_chain_by_value(next_word)
            if len(chain_piece) > 0:
                prob = lib.classes.chain_tools.make_probability(chain_piece[0]["links"])
                next_word = lib.classes.chain_tools.roll_the_dice(prob)
                chain += " " + next_word
            else:
                chain.rstrip()
                chain += "!"
        return chain

    def _random_tweet_seed(self, mongo_connector):
        seed = mongo_connector.get_random_tweet_text()
        split = seed.split()
        while not split[0][0].isupper():
            split = mongo_connector.get_random_tweet_text().split()
        return split[0]

