from collections import defaultdict
from io import StringIO
import re

test = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

pattern = re.compile(r"([0-9]+)")
total = 0
totals = defaultdict(int)

# with StringIO(test) as data:
with open("input4.txt") as data:
  for card, line in enumerate(data):
    totals[card] += 1
    winning, entries = line.strip()[line.index(":"):].split("|")
    wnumbers = set(pattern.findall(winning))
    enumbers = set(pattern.findall(entries))

    overlap = wnumbers & enumbers
    if len(overlap) > 0:
      score = 2 ** (len(overlap) - 1)
      total += score
      # print(score, "->", total, "/", line[:line.index(":")], overlap)

      for next_ in range(card+1, card + len(overlap) + 1):
        totals[next_] += max(1, totals[card])
  
for extra in range(card+1, max(totals)+1):
  del totals[extra]

print("Part 1:", total)
print("Part 2:", sum(totals.values()))