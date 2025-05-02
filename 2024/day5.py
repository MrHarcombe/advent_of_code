from collections import defaultdict
from io import StringIO

test = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

def sort_invalid_values(values):
    new_values = [values.pop(0)]
    for value in values:
        if value in rules:
            for nvi in range(len(new_values)):
                if new_values[nvi] in rules[value]:
                    new_values.insert(nvi, value)
                    break
            else:
                new_values.append(value)
        else:
            new_values.append(value)
    
    return new_values

rules = defaultdict(list)
valid_middles = 0
invalid_middles = 0

# with StringIO(test) as input_data:
with open("input5.txt") as input_data:
    for line in input_data:
        if "|" in line:
            before, after = map(int, line.strip().split("|"))
            rules[before].append(after)
            
        elif "," in line:
            values = list(map(int, line.strip().split(",")))
            valid = True
            for i, num in enumerate(values, 1):
                if not valid:
                    break
                
                for pre in values[:i]:
                    if num in rules and pre in rules[num]:
                        valid = False
                        new_values = sort_invalid_values(values)
                        invalid_middles += new_values[len(values) // 2]
                        break

            if valid:
                valid_middles += values[len(values) // 2]
                        
print("Part 1:", valid_middles)
print("Part 2:", invalid_middles)
