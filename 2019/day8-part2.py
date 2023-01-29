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

#print(pixels)

image = []
for pixel in range(len(pixels[0])):
  for layer in range(len(pixels)):
    if pixels[layer][pixel] != '2':
      image.append('#' if pixels[layer][pixel] == '1' else ' ')
      break

for row in range(0, len(image), width):
  print(''.join(image[row:row+width]))
