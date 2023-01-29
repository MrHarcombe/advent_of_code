from io import StringIO

test = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

with StringIO(test) as f:
#with open("input1.txt") as f:
    totals = []
    amount = 0
    
    for line in f:
        if line.strip() != "":
            amount += int(line)
            
        else:
            totals.append(amount)
            amount = 0
    
    if amount != 0:
        totals.append(amount)
    
    print("top:", max(totals))
    print("top 3:", sum(sorted(totals)[-3:]))
