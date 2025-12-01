from functools import cache
from time import time

serial = 2694

@cache
def calculate_fuel_cell(x,y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial
    power_level *= rack_id
    power_level %= 1000
    power_level //= 100
    power_level -= 5

    return power_level

def calculate_battery_level(x,y,size):
    if size > 1:
        score = calculate_battery_level(x,y,size-1)
        for dy in range(size-1):
            score += calculate_fuel_cell(x+size-1, y+dy)
        for dx in range(size):
            score += calculate_fuel_cell(x+dx, y+size-1)
        return score

    else:
        return calculate_fuel_cell(x, y)

best = 0
best_xy = None

start = time()
for size in range(1,50):
    for y in range(1,301-size):
        for x in range(1,301-size):
            score = calculate_battery_level(x,y,size)

            if score > best:
                best = score
                best_xy = (x,y,size)

    print("Completed size", size, f"({best_xy})")

print("Elapsed:", time() - start)
print("Best:", best, "at:", best_xy)
