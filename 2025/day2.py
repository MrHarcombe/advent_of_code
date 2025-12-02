from io import StringIO

import re

def part1(product_ranges):
    invalid_ids = 0

    for product_range in product_ranges:
        for product_id in product_range:
            str_id = str(product_id)
            len_id = len(str_id)

            if len_id >= 2 and len_id % 2 == 0 and str_id[:len_id // 2] == str_id[len_id // 2:]:
                invalid_ids += product_id
                # print("Invalid id:", product_id)

    return invalid_ids

def part2(product_ranges):
    invalid_ids = 0

    for product_range in product_ranges:
        for product_id in product_range:
            # print("Product id:", product_id)
            str_id = str(product_id)
            len_id = len(str_id)

            for part in range(1, len_id // 2 + 1):
                #print("Trying", str_id[:part])
                if re.match(f"({str_id[:part]})+$", str_id):
                    invalid_ids += product_id
                    # print("Invalid id:", product_id)
                    break
                    
    return invalid_ids

test = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

product_ranges = []

# with StringIO(test) as data:
with open("input2.txt") as data:
    for line in data:
        # print(line)
        for products in line.split(","):
            # print(products)
            begin, end = map(int, products.split("-"))
            product_ranges.append(range(begin, end+1))
            

print("Part 1:", part1(product_ranges))
print("Part 2:", part2(product_ranges))
