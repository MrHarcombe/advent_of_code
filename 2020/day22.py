from io import StringIO

test = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

test = """Player 1:
43
19

Player 2:
2
29
14"""

def read_hand(handle):
    hand = []
    handle.readline()
    while True:
        card = handle.readline()
        if len(card.strip()):
            hand.append(int(card))
        else:
            break
            
    return hand

# with StringIO(test) as inputs:
with open("input22.txt") as inputs:
    hand1 = read_hand(inputs)
    hand2 = read_hand(inputs)


def normal_game(hand1, hand2):
    while len(hand1) and len(hand2):
        card1 = hand1.pop(0)
        card2 = hand2.pop(0)
        
        if card1 > card2:
            hand1 += [card1, card2]
        else:
            hand2 += [card2, card1]

    return hand1, hand2

def recursive_game(hand1, hand2):
    previous_hands = set()
    
    while len(hand1) and len(hand2):
        base_case_check = (",".join(map(str,hand1)), ",".join(map(str,hand2)))
        
        if base_case_check in previous_hands:
            return hand1, hand2
        
        else:
            previous_hands.add(base_case_check)

            card1 = hand1.pop(0)
            card2 = hand2.pop(0)
            
            if card1 <= len(hand1) and card2 <= len(hand2):
                sub_hand1, sub_hand2 = recursive_game(hand1[:card1], hand2[:card2])
                if len(sub_hand1):
                    hand1 += [card1, card2]
                else:
                    hand2 += [card2, card1]

            else:
                if card1 > card2:
                    hand1 += [card1, card2]
                else:
                    hand2 += [card2, card1]

    return hand1, hand2

def score_hand(hand):
    score = 0
    for pos, mult in enumerate(range(len(hand), 0, -1)):
        score += hand[pos] * mult

    return score

# end1, end2 = normal_game(list(hand1), list(hand2))
# winning_hand = end1 if len(end1) else end2
# print("Part 1:", score_hand(winning_hand))

end1, end2 = recursive_game(list(hand1), list(hand2))
winning_hand = end1 if len(end1) else end2
print("Part 2:", score_hand(winning_hand))

# 31029 too low
