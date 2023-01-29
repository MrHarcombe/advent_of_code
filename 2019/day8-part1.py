width = 25
height = 6

pixels = []
line = ""

with open("input.txt") as f:
  line = f.readline()
  #line = "123456789012"

block = width * height
for chunk in range(0,len(line),block):
  pixels.append(line[chunk:chunk+block])

print(pixels)
counts = [(row.count('0'), row) for row in pixels]
print(min(counts))
print("1s:", min(counts)[1].count('1'))
print("2s:", min(counts)[1].count('2'))
print(min(counts)[1].count('1') * min(counts)[1].count('2'))
