from io import StringIO
import re

test = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

bag_pattern = re.compile(r"((\d*) ?(\w+ \w+)) bag")

holding_bags = {}

# with StringIO(test) as data:
with open("input7.txt") as data:
    for line in data:
        bags = bag_pattern.findall(line.strip())
        holding_bags[bags[0][2]] = [(bag, int(count)) if len(count) > 0 else (None) for (_, count, bag) in bags[1:]]

def check_bag(bag):
    # print("contains", end=" ")
    if bag == "shiny gold":
        # print("shiny gold", end="!!!")
        return True
    
    # print(bag, end=", ")

    response = False
    for sub_bag in holding_bags[bag]:
        if sub_bag is not None:
            response |= check_bag(sub_bag[0])
            
    return response

p1_total = 0
for bag in holding_bags:
    if bag != "shiny gold":
        # print("Checking:", bag, end=" ")
        if check_bag(bag):
            # print(bag, "can contain a shiny gold")
            p1_total += 1
        # print()

print("Part 1:", p1_total)

def count_bags(bag, count):
    sub_total = 0
    
    for sub_bag in holding_bags[bag]:
        if sub_bag is not None:
            sub_bag, sub_count = sub_bag
            sub_total += count * (sub_count + count_bags(sub_bag, sub_count))

    return sub_total

p2_total = 0
for bag, count in holding_bags["shiny gold"]:
    p2_total += count + count_bags(bag, count)

print("Part 2:", p2_total)
