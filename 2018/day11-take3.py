from time import time

serial = 2694

def calculate_fuel_cell(x,y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial
    power_level *= rack_id
    power_level %= 1000
    power_level //= 100
    power_level -= 5

    return power_level

def fill_summed_area(fuel_cells,summed_area):
    for y in range(300):
        for x in range(300):
            summed_area[y][x] = fuel_cells[y][x] + (summed_area[y-1][x] if y > 0 else 0) + (summed_area[y][x-1] if x > 0 else 0) - (summed_area[y-1][x-1] if y > 0 and x > 0 else 0)

fuel_cells = [[calculate_fuel_cell(x,y) for x in range(300)] for y in range(300)]
summed_area = [[None for _ in range(300)] for _ in range(300)]

fill_summed_area(fuel_cells, summed_area)

def calculate_battery_level(x,y,size,summed_area):
    try:
        return summed_area[y][x] + summed_area[y+size][x+size] - summed_area[y+size][x] - summed_area[y][x+size]
    except:
        return 0

start = time()
best = max((calculate_battery_level(x,y,size,summed_area),x+1,y+1,size) for size in range(1,301) for y in range(1,301-size) for x in range(1,301-size))
print("Elapsed:", time() - start)
print("Best:", best[0], "at:", best[1:])
