import itertools

names = set()
preferences = {}

with open("input.txt") as f:
  line = f.readline()

  while line != "":
    name1, rest = line.split("would") 
    amount, rest = rest.split("happiness")
    rest, name2 = rest.split("to")

    name1 = name1.strip()
    name2 = name2.strip()[:-1]
    amount = int(amount.strip().replace("gain ", "").replace("lose ", "-"))
    names.add(name1)
    preferences[name1+name2] = amount

    line = f.readline()

print(names, len(names))
print(preferences, len(preferences))

for name in names:
  preferences[name+'You'] = 0
  preferences['You'+name] = 0

names.add('You')

best = 0
for places in itertools.permutations(names):
  #print(places, end=": ")
  total = 0
  for i in range(len(places)):
    total += preferences[places[i] + places[(i+1) % len(places)]]
    total += preferences[places[(i+1) % len(places)] + places[i]]

  #print(total)
  if total > best:
    print(places, total)
    best = total

print("Optimal:", best)