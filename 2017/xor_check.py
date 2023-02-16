values = [65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22]

value = values[0]
for j in range(0+1, 0+16):
    value ^= values[j]
    
print(f"{value:02x}")