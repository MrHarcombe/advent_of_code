total_needed = 0

with open("input.txt") as f:
  gift = f.readline()
  while gift != "":
    l,w,h = map(int, gift.split("x"))
    sa = 2*l*w + 2*w*h + 2*h*l
    smallest = min(l*w, w*h, h*l)
    total_needed += sa + smallest
    gift = f.readline()

print(total_needed)
