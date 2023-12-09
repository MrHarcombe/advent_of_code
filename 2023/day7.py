from collections import Counter
from io import StringIO
from time import time

test = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

cards = "23456789TJQKA"
p2_cards = "J23456789TQKA"

def hand_value_card_values(cards_bid):
    hand, bid = cards_bid
    hand_count = Counter(hand)
    counts = hand_count.most_common()
    if counts[0][1] > 3:
        rank = counts[0][1] + 2
    elif counts[0][1] == 3 and counts[1][1] == 2:
        rank = 5
    elif counts[0][1] == 3:
        rank = 4
    elif counts[0][1] == 2 and counts[1][1] == 2:
        rank = 3
    elif counts[0][1] == 2:
        rank = 2
    else:
        rank = 1
    
    return [rank] + [cards.index(card) for card in hand]

def hand_value_card_values_2(cards_bid):
    hand, bid = cards_bid
    hand_count = Counter(hand)
    counts = hand_count.most_common()
    if hand_count["J"] > 0:
        if len(hand_count) > 1:
            add_to = 0
            if counts[0][0] == "J":
                add_to = 1
            hand_count[counts[add_to][0]] += hand_count["J"]
            del hand_count["J"]
            counts = hand_count.most_common()
    if counts[0][1] > 3:
        rank = counts[0][1] + 2
    elif counts[0][1] == 3 and counts[1][1] == 2:
        rank = 5
    elif counts[0][1] == 3:
        rank = 4
    elif counts[0][1] == 2 and counts[1][1] == 2:
        rank = 3
    elif counts[0][1] == 2:
        rank = 2
    else:
        rank = 1

    return [rank] + [p2_cards.index(card) for card in hand]

hands = []
bids = []

# with StringIO(test) as data:
start = time()
with open("input7.txt") as data:
    for line in data:
        hand, bid = line.strip().split()
        hands.append(hand)
        bids.append(bid)

bids = list(map(int, bids))
camel = sorted(zip(hands, bids), key=hand_value_card_values)
camel_2 = sorted(zip(hands, bids), key=hand_value_card_values_2)

print("Parsing:", time() - start)
start = time()
print("Part 1:", sum([(i+1) * bid for i, (hand,bid) in enumerate(camel)]))
print("Elapsed:", time() - start)
start = time()
print("Part 2:", sum([(i+1) * bid for i, (hand,bid) in enumerate(camel_2)]))
print("Elapsed:", time() - start)