banks = []

with open("banks.txt") as file:
  banks = [int(n) for n in file]
