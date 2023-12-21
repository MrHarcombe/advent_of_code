from collections import defaultdict
from io import StringIO
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
    return operators[operator], component, value, outcome

# with StringIO(test) as data:
with open("input19.txt") as data:
    line = data.readline().strip()
    while line != "":
        m = workflow_pattern.findall(line)
        workflow, rules = m[0]
        # print(workflow, rules.split(","))
        workflows[workflow] += [interpret_rule(r) for r in rules.split(",")]
        line = data.readline().strip()

    line = data.readline().strip()
    while line != "":
        parts.append([int("".join(n)) for n in parts_pattern.findall(line)])
        line = data.readline().strip()

xmas = {"x": 0, "m": 1, "a": 2, "s": 3}

accepted = []
for part in parts:
    current_workflow = "in"
    while current_workflow not in ("A", "R"):
        workflow = workflows[current_workflow]
        for step in workflow:
            if type(step) == str:
                current_workflow = step
                break

            operator, component, value, outcome = step
            if operator(part[xmas[component]], value):
                current_workflow = outcome
                break
            
        if current_workflow == "A":
            accepted.append(sum(part))

print("Part 1:", sum(accepted))
