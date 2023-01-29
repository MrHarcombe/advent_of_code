inputs = """199
200
208
210
200
207
240
269
260
263"""

depths = []
with open("input1.txt") as inputs:
    depths = inputs.readlines()

previous = None
count = 0

for i in range(0,len(depths)):
    value = sum([int(n) for n in depths[i:i+3] if i+3 <= len(depths)])
    if previous and value > previous:
        count += 1
    previous = value

print(count)