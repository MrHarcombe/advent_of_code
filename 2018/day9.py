from collections import defaultdict, deque
from io import StringIO

test = """9 players; last marble is worth 25 points""" # high score is 32
test = """10 players; last marble is worth 1618 points""" # high score is 8317
test = """13 players; last marble is worth 7999 points""" # high score is 146373

actual = """493 players; last marble is worth 71863 points"""
actual2 = """493 players; last marble is worth 7186300 points"""

with StringIO(actual) as data:
    for line in data:
        tokens = line.split()
        players = int(tokens[0])
        last = int(tokens[-2])
        
# print(players, last)

scores = defaultdict(int)
circle = deque([0])
current = 0
next_marble = 1
current_player = 0

while next_marble <= last:
    if len(circle) == 1:
        circle.append(next_marble)
        current = len(circle) - 1

    elif next_marble % 23 == 0:
        current -= 7
        current %= len(circle)
        scores[current_player] += next_marble + circle[current]
        circle.remove(circle[current])

    else:
        current += 1
        current %= len(circle)
        current += 1
        circle.insert(current, next_marble)
        
    next_marble += 1
    current_player += 1
    current_player %= players

print("Part 1:", max(scores.values()))