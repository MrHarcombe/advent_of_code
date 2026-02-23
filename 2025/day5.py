from io import StringIO

test = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

def reduce_product_ranges(product_ranges):
    made_change = True
    while made_change:
        made_change = False
        
        amended_range = None
        for candidate in range(len(product_ranges)):
            product_range = product_ranges.pop(0)
            start = product_range.start
            stop = product_range.stop
            
            for index in range(len(product_ranges)):
                if start >= product_ranges[index].start and stop <= product_ranges[index].stop:
                    # new range is irrelevant
                    amended_range = range(product_ranges[index].start, product_ranges[index].stop)
                    break
                elif start <= product_ranges[index].start and stop >= product_ranges[index].stop:
                    # old range is irrelevant
                    amended_range = range(start, stop)
                    break
                elif start >= product_ranges[index].start and start <= product_ranges[index].stop:
                    # new range extends beyond end of current range
                    amended_range = range(product_ranges[index].start, stop)
                    break
                elif stop <= product_ranges[index].stop and stop >= product_ranges[index].start:
                    # new range extend beyond beginning of current range
                    amended_range = range(start, product_ranges[index].stop)
                    break
            else:
                product_ranges.append(product_range)

            if amended_range is not None:
                del product_ranges[index]
                product_ranges.append(amended_range)
                made_change = True

    return product_ranges

product_ranges = []
ingredient_count = 0

# with StringIO(test) as file:
with open("input5.txt") as file:
    for line in file:
        if "-" not in line:
            break

        start, stop = map(int, line.strip().split("-"))
        product_ranges.append(range(start, stop+1))
    
    for line in file:
        ingredient = int(line)
        for product_range in product_ranges:
            if ingredient in product_range:
                ingredient_count += 1
                break
            
print("Part 1:", ingredient_count)

reduced_ranges = reduce_product_ranges(list(product_ranges))
all_ingredients = 0
for product_range in reduced_ranges:
    all_ingredients += len(product_range)
print("Part 2:", all_ingredients)

# 355373167127369 too high