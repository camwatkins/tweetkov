import random


def make_probability(links):
    prob_set =[]  

    total = sum(int(link["count"]) for link in links)

    for link in links:
        prob_set.append({"value": link["value"], "probability": float(float(link["count"]) / total)})

    return prob_set


def roll_the_dice(set):
    roll = random.uniform(0.0, 1.0)

    for item in set:
        roll -= item["probability"]
        if roll <= 0:
            return item["value"] 

