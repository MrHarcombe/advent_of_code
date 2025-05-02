from io import StringIO

def replace_subrule(rule):
    rule_parts = rule.split()
    for i in range(len(rule_parts)):
        if rule_parts[i].isdigit():
            sub_rule = rule_parts[i]
            break

    prefix = " ".join(rule_parts[:i])
    suffix = " ".join(rule_parts[i+1:])

    new_rules = []
    for part in rules[sub_rule].split("|"):
        new_rules.append(prefix + " " + part + " " + suffix)

    return new_rules

test = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb'''

rules = {}
terminals = {}
possibles = []

# with StringIO(test) as data:
with open("input19.txt") as data:
    for line in data:
        if len(line.strip()) > 0:
            if ":" in line:
                rule, content = line.strip().split(":")
                if '"' in content:
                    terminals[rule] = content.replace('"', '')
                    rules[rule] = content.replace('"', '')
                else:
                    rules[rule] = content.strip()
            else:
                possibles.append(line.strip())

for k in rules:
    for t in terminals:
        rules[k] = rules[k].replace(t, terminals[t])

expansions = set()
queue = [rules["0"]]
while len(queue) > 0:
    rule = queue.pop(0)
    alts = replace_subrule(rule)
    for alt in alts:
        if alt.replace(" ", "").isalpha():
            expansions.add(alt.replace(" ", ""))
        else:
            queue.append(alt)

count = 0
for possible in possibles:
    if possible not in expansions:
        count += 1
        print(possible, "not in expansions")
print(count, "possibles do not match")