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

orbit_count = 0

for p in orbits:
  matches = []
  if p != 'COM':
    matches = find_in_orbits(p)
    for match in matches:
      #print(match)
      if match != 'COM':
        matches += find_in_orbits(match)

  orbit_count += len(matches)
  #print("orbit_count:", orbit_count)

print("final orbit_count:", orbit_count)