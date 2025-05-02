from io import StringIO

test = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

categories = {}
scanning_error_rate = 0

valid_tickets = []
your_ticket = []

# with StringIO(test) as data:
with open("input16.txt") as data:
    line = data.readline()
    nearby = False
    while line != "":
        if line.startswith("your ticket:"):
            your_ticket = list(map(int, data.readline().strip().split(",")))

        elif line.startswith("nearby tickets:"):
            nearby = True

        elif nearby:
            # all_ranges = []
            # for entry in categories.values():
            #     all_ranges.extend(entry)

            valid = True
            ticket = list(map(int, line.strip().split(",")))
            for value in ticket:
                if not any([value in rng for rng in categories.values()]):
                    scanning_error_rate += value
                    valid = False

            if valid:
                valid_tickets.append(ticket)

        elif len(line.strip()) > 0:
            category, values = line.strip().split(":")
            ranges = set()
            for rng in values.split(" or "):
                bounds = list(map(int, rng.split("-")))
                ranges = ranges.union(range(bounds[0], bounds[1] + 1))
            categories[category.replace(" ", "_")] = ranges

        line = data.readline()

# print(categories)
print("Part 1:", scanning_error_rate)

possibles = {k: [] for k in categories}
for i in range(len(your_ticket)):
    i_values = [your_ticket[i]] + [ticket[i] for ticket in valid_tickets]
    for k, v in categories.items():
        if all(tv in v for tv in i_values):
            possibles[k].append(i)

all_known = {}
some_known = [key for key in possibles if len(possibles[key]) == 1]
while len(some_known) > 0:
    known = some_known[0]
    all_known[known] = possibles[known][0]
    del possibles[known]
    known_value = all_known[known]
    for poss in possibles:
        possibles[poss].remove(known_value)
    some_known = [key for key in possibles if len(possibles[key]) == 1]

ticket_fields = 1
for k, v in all_known.items():
    if k.startswith("departure"):
        ticket_fields *= your_ticket[v]

print("Part 2:", ticket_fields)
