from unittest import TestCase
import lib.classes.chain_tools as chain_tools


class Test(TestCase):
    def test_make_probability(self):
        links = [{
            "value": "a",
            "count": 2
        }, {
            "value": "test",
            "count": 2
        }]
        prob_set = chain_tools.make_probability(links)
        assert prob_set[0]["probability"] == float(0.5)
        assert prob_set[1]["probability"] == float(0.5)

    def test_roll_the_dice(self):
        self.fail()
