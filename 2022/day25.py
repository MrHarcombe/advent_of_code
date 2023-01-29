from io import StringIO
from math import ceil, floor, log

test = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

def decode_snafu(snafu):
    snaful = list(snafu)
    total = 0
    col_value = 1
    while len(snaful) > 0:
        column = snaful.pop()
        if column.isdigit():
            total += int(column) * col_value
        elif column == "-":
            total -= col_value
        elif column == "=":
            total -= 2 * col_value
        col_value *= 5

    return total

def encode_snafu(value):
    def max_snafu(power):
        if power == 0:
            return 2
        elif power < 0:
            return 0
        else:
            return int("2" * (power+1), 5)
            
    snafu = []

    col_place = ceil(log(value, 5))
    if max_snafu(col_place-1) < value:
        col_place += 1
    
    for power in range(col_place-1, -1, -1):
        if value > 0:
            rhs = max_snafu(power-1)
            for pv in (2,1,0):
                lhs = pv * 5 ** power
                if -rhs <= lhs - value <= rhs:
                    value -= pv * 5 ** power
                    snafu.append(str(pv))
                    break
        elif value < 0:
            next_max = max_snafu(power-1)
            if -next_max <= value + 5 ** power <= next_max:
                value += 5 ** power
                snafu.append("-")
            elif -next_max <= value + 2 * 5 ** power <= next_max:
                value += 2 * 5 ** power
                snafu.append("=")
            else:
                # print("uh-oh <0")
                snafu.append("0")
        else:
            # print("uh-oh =0")
            snafu.append("0")

    return "".join(snafu)

total = 0
# with StringIO(test) as f:
with open("input25.txt") as f:
    for line in f:
        value = line.strip()
        # print(value,"->", decode_snafu(value))
        total += decode_snafu(value)
        
print("Total:", total) # 33411698619881
print("SNAFU total:", encode_snafu(total)) # 2---0-1-2=0=22=2-011
