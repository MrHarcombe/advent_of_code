from io import StringIO
from string import ascii_lowercase
from time import time

original = "dabAcCaCBAcCcaDA"

def react(polymer):
  new_polymer = polymer
  for i in range(len(polymer)-1):
    if abs(ord(polymer[i]) - ord(polymer[i+1])) == 32:
      new_polymer = polymer.replace(f"{polymer[i]}{polymer[i+1]}", "")
      break
  return new_polymer

# print(test)
# print(react(test))
polymer = original

with open("input5.txt") as data:
  original = data.readline().strip()

polymer = str(original)
start = time()
before = 0
after = len(polymer)
while before != after:
  before = after
  polymer = react(polymer)
  after = len(polymer)
end = time()

# print("Part 1:", after, polymer)
print("Part 1:", after)
print("Elapsed:", end - start)

min_react = float("inf")
min_polymer = None
start = time()
for ch in ascii_lowercase:
  # print("Trying", ch, "...")
  polymer = original.replace(ch, "")
  polymer = polymer.replace(ch.upper(), "")

  before = 0
  after = len(polymer)
  while before != after:
    before = after
    polymer = react(polymer)
    after = len(polymer)

  if after < min_react:
    min_react = after
    min_polymer = polymer
end = time()

# print("Part 2:", min_react, min_polymer)
print("Part 2:", min_react)
print("Elapsed:", end - start)
