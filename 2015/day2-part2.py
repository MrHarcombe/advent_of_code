total_needed = 0

with open("input.txt") as f:
  gift = f.readline()
  while gift != "":
    l,w,h = map(int, gift.split("x"))

    # paper
    #sa = 2*l*w + 2*w*h + 2*h*l
    #smallest = min(l*w, w*h, h*l)
    #total_needed += sa + smallest

    # ribbon
    wrap = 2 * (l+w+h) - 2 * max(l,w,h)
    bow = l*w*h
    total_needed += wrap + bow
    gift = f.readline()

print(total_needed)
