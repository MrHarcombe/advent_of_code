from itertools import product

serial = 2694
fuel_cells = {}
battery_cache = {}

best = 0
best_xy = (0,0)

for y in range(1,301):
    for x in range(1,301):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += serial
        power_level *= rack_id
        power_level %= 1000
        power_level //= 100
        power_level -= 5

        if power_level > best:
            best = power_level
            best_xy = (x,y,1)

        fuel_cells[(x,y)] = power_level
        battery_cache[(x,y,1)] = power_level

for size in range(1,301):
    for y in range(1,301-size):
        for x in range(1,301-size):
            if (x,y,size-1) in battery_cache:
                try:
                    score = battery_cache[(x,y,size-1)]
                    for dy in range(size-1):
                        score += fuel_cells[(x+size-1, y+dy)]
                    for dx in range(size):
                        score += fuel_cells[(x+dx, y+size-1)]
                    
                    battery_cache[(x,y,size)] = score
                    
                    if score > best:
                        best = score
                        best_xy = (x,y,size)

                except KeyError as ke:
                    print("Failed with", ke.args, "using", (x,y,size), "and", (dx,dy))

            else:
                # print("Missing cache:", (x,y,size-1))

                score = 0
                for dy in range(size):
                    for dx in range(size):
                        score += fuel_cells[(x+dx, y+dy)]
                
                battery_cache[(x,y,size)] = score
                
                if score > best:
                    best = score
                    best_xy = (x,y,size)
                

    print("Completed size", size, f"({best_xy})")

print("Best:", best, "at:", best_xy)
