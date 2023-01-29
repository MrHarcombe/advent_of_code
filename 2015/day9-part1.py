import itertools

routes = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141""".split("\n")

distances = {}
places = set()

def get_trip(from_, to):
  if (from_, to) in distances:
    return distances[(from_,to)]
  else:
    return distances[(to,from_)]

#Trouble77
#82689

def get_distance(route):
  distance = 0
  for i in range(len(route)-1):
    distance += get_trip(route[i], route[i+1])

  #print(route,"->",distance)
  return distance

with open("input.txt") as f:
  routes = f.readlines()

for route in routes:
  parts = route.split("=")
  dests = parts[0].split("to")
  distances[(dests[0].strip(), dests[1].strip())] = int(parts[1])
  places.add(dests[0].strip())
  places.add(dests[1].strip())

#print(distances)
#print(places)

print(min([get_distance(route) for route in itertools.permutations(places,len(places))]))
print(max([get_distance(route) for route in itertools.permutations(places,len(places))]))