orbits = {}

def find_in_orbits(name):
  found = [o[0] for o in orbits.items() if name in o[1]]
  #print("For:", name, "Found:", found)

  return found

with open("inputs.txt") as f:
  orbit = f.readline()

  while orbit != "":
    left, right = orbit.strip().split(")")
    #print(left, "->", right)

    if left in orbits:
      orbits[left].append(right)
    else:
      orbits[left] = [right]

    if right not in orbits:
      orbits[right] = []

    orbit = f.readline()

print(orbits)

from_you = find_in_orbits("YOU")
for planet in from_you:
  from_you += find_in_orbits(planet)

total_hops = 0

from_san = find_in_orbits("SAN")
for planet in from_san:
  try:
    total_hops = from_you.index(planet)
    break
  except ValueError:
    from_san += find_in_orbits(planet)

#print(from_you[:total_hops])
#print(from_san)

total_hops += len(from_san) - 1
print("total_hops", total_hops)