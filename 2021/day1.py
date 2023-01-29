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

with open("input1.txt") as inputs:
    previous = None
    count = 0
    for depth in inputs:
        value = int(depth.strip())
        if previous and value > previous:
            count += 1
        previous = value
        
print(count)