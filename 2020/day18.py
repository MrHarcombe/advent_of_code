from io import StringIO
from operator import add, mul

ops = {"+": add, "*": mul}

def resolve_brackets(expr):
    start = len(expr) - expr[::-1].index("(") - 1
    end = expr.index(")", start)

    # value in the right-most bracket
    sub_total = resolve_expression(expr[start+1:end])

    return expr[:start] + [sub_total] + expr[end+1:]

def total_subexpression(expr):
    total = int(expr[0])
    for i in range(1, len(expr), 2):
        total = ops[expr[i]](total, int(expr[i+1]))

    return total

def resolve_expression(expr):
    if "(" in expr:
        return resolve_expression(resolve_brackets(expr))

    return total_subexpression(expr)

test = """1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

total = 0
# with StringIO(test) as data:
with open("input18.txt") as data:
    for line in data:
        parts = line.replace("(", "( ").replace(")", " )").split()
        total += resolve_expression(parts)

print(total)