low=347312
high=805915

#low = 555556
#high = 555559

possibles = []

def check_adjacent(check):
  return check[0] == check[1] or check[1] == check[2] or check[2] == check[3] or check[3] == check[4] or check[4] == check[5]

def check_ascent(check):
  return check[0] <= check[1] and check[1] <= check[2] and check[2] <= check[3] and check[3] <= check[4] and check[4] <= check[5]


for possible in range(low, high+1):
  check = str(possible)
  if check_adjacent(check) and check_ascent(check):
    possibles.append(check)

#print(possibles)
print(len(possibles))