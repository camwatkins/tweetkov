import time
import threading


class VotingBooth(object):
    def __init__(self, candidates=None):
        if candidates is None:
            candidates = []
        self._now_voting = False
        self._voting_candidates = self._add_candidates(candidates)

    def _add_candidates(self, candidates):
        category_candidates = []
        for index, candidate in enumerate(candidates, start=0):
            category_candidates.insert(
                index, {
                    "candidate": candidate,
                    "vote_count": 0
                }
            )
        return category_candidates

    def start_voting(self, candidates, interval=30):
        self._candidates = self._add_candidates(candidates)
        self._now_voting = True

    def vote(self, pick):
        if self._now_voting and len(self._candidates) > 0:
            try:
                self._candidates[int(pick)]["vote_count"] = self._candidates[int(pick)]["vote_count"] + 1
            except ValueError:
                return
        return

    def results(self):
        highest_count = -1
        current_highest = None
        for candidate in self._candidates:
            if candidate["vote_count"] >= highest_count:
                highest_count = candidate["vote_count"]
                current_highest = candidate["candidate"]
        return current_highest

    def stop_voting(self):
        self._now_voting = False

    def is_voting(self):
        return self._now_voting



