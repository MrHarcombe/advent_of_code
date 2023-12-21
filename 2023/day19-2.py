from collections import defaultdict
from io import StringIO
from itertools import combinations
from math import prod
from operator import lt, gt
import re

test = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

# test = """one{x>8:R,two}
# two{x<7:A,R}
# in{x>3:A,R}"""

workflow_pattern = re.compile(r"([a-z]+){(.+)}")
rule_pattern = re.compile(r"([a-z]+)([^0-9]+)([0-9]+)")
parts_pattern = re.compile(r"(?:x=(?P<x>[0-9]+)|m=(?P<m>[0-9]+)|a=(?P<a>[0-9]+)|s=(?P<s>[0-9]+))+")

operators = {"<": lt, ">": gt}

workflows = defaultdict(list)
parts = []

def interpret_rule(rule_string):
    if ":" not in rule_string:
        return rule_string
    
    condition, outcome = rule_string.split(":")
    m = rule_pattern.match(condition)
    component = m.group(1)
    operator = m.group(2)
    value = int(m.group(3))
    return operator, component, value, outcome

##
# from https://stackoverflow.com/questions/32480423/how-to-check-if-a-range-is-a-part-of-another-range-in-python-3-x
#
def range_subset(range1, range2):
    """Whether range1 is a subset of range2."""
    if not range1:
        return True  # empty range is subset of anything
    if not range2:
        return False  # non-empty range can't be subset of empty range
    if len(range1) > 1 and range1.step % range2.step:
        return False  # must have a single value or integer multiple step
    return range1.start in range2 and range1[-1] in range2

# with StringIO(test) as data:
with open("input19.txt") as data:
    line = data.readline().strip()
    while line != "":
        m = workflow_pattern.findall(line)
        workflow, rules = m[0]
        # print(workflow, rules.split(","))
        workflows[workflow] += [interpret_rule(r) for r in rules.split(",")]
        line = data.readline().strip()

xmas = {"x": 0, "m": 1, "a": 2, "s": 3}

# parts_ranges = [("in", ((range(1, 11), range(1, 2), range(1, 2), range(1, 2))))]
parts_ranges = [("in", ((range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001))))]
accepted = []
while len(parts_ranges) > 0:
    current_workflow, parts = parts_ranges.pop(0)

    if current_workflow == "A":
        accepted.append(prod(len(p) for p in parts))
        # accepted.append(parts)
        # append = True
        # to_remove = []
        # for i in range(len(accepted)):
        #     a = accepted[i]
        #     if all(range_subset(a[p], parts[p]) for p in range(4)):
        #         to_remove.append(i)
        #         print("Removing...", accepted[i])
        #     elif all(range_subset(parts[p], a[p]) for p in range(4)):
        #         append = False
        #         print("Not appending...", parts)
        #         
        # if len(to_remove) > 0:
        #     for i in sorted(to_remove, reverse=True):
        #         print("Deleting accepted...", i)
        #         del accepted[i]
        # if append:
        #     print("Appending...", parts)
        #     accepted.append(parts)
        continue
    elif current_workflow == "R":
        continue
    
    # while current_workflow not in ("A", "R"):
    workflow = workflows[current_workflow]
    for step in workflow:
        if type(step) == str:
            parts_ranges.append((step, parts))
            # current_workflow = step
            break

        operator, component, value, outcome = step
        current_range = parts[xmas[component]]
        if operator == "<":
            # time to think about splitting the range...
            if current_range.stop < value:
                # all falls within range, no splitting, just move all to
                # the new workflow
                parts_ranges.append((step, parts))

            elif current_range.start < value:
                # only the start falls within the range, split and let the
                # upper half continue onto the next step
                part1 = list(parts)
                part1[xmas[component]] = range(current_range.start, value)
                parts_ranges.append((outcome, part1))

                part2 = list(parts)
                part2[xmas[component]] = range(value, current_range.stop)
                parts = part2

            else:
                # none of it falls within the range, so do nothing and let
                # it move onto the next step
                pass

        elif operator == ">":
            # time to think once again about splitting the range...
            if current_range.stop < value:
                pass

            elif current_range.start < value:
                # split and let the lower half continue onto the next step,
                # but move the upper half onto the new workflow
                part1 = list(parts)
                part1[xmas[component]] = range(current_range.start, value+1)
                parts = part1

                part2 = list(parts)
                part2[xmas[component]] = range(value+1, current_range.stop)
                parts_ranges.append((outcome, part2))

            else:
                # all falls within range, no splitting, just move all to
                # the new workflow
                parts_ranges.append((step, parts))

        else:
            print("Uh-oh", operator)

# total = 0
# for a in accepted:
#     print(a)
#     total += prod(len(p) for p in a)

print("Part 2:", sum(accepted))
# print("Part 2:", accepted)

## Part 2
# 131905707819724 too high
