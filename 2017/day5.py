jumps = []
with open("input5.txt") as file:
  jumps = [int(n) for n in file]

print(jumps)

current = 0
next = 0
count = 0

#print(current, jumps[current])
while current in range(len(jumps)):
  next = jumps[current]
  if next >= 3:
    jumps[current] -= 1
  else:
    jumps[current] += 1
  current += next
  count += 1

print(count)
