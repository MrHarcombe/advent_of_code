import io

test = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

seabed = {}

# with io.StringIO(test) as vents:
with open('input5.txt') as vents:
    for vent in vents:
        start, end = vent.strip().split(' -> ')
        x1,y1 = [int(n) for n in start.split(',')]
        x2,y2 = [int(n) for n in end.split(',')]

        print((x1,y1),(x2,y2), end = ' ')

        if x1 == x2 or y1 == y2:
            print('straight')
            for x in range(min(x1,x2), max(x1,x2)+1):
                for y in range(min(y1,y2), max(y1,y2)+1):
                    if (x,y) in seabed:
                        seabed[(x,y)] += 1
                    else:
                        seabed[(x,y)] = 1
        else:
            # diagonals, 4 cases
            # - x1,y1 both less than x2,y2 - so loop needs to increase by 1,1
            # - x1,y2 both more than x2,y2 - so loop needs to decrease by 1,1
            # - x1 < x2 but y1 > y2 - so loop needs to run as 1,-1
            # - x1 > x2 but y1 < y2 - so loop needs to run as -1,1
            if x1<x2 and y1<y2:
                print('diagonal 1,1')
                y = y1
                for x in range(x1,x2+1):
                    pos = (x,y)
                    if pos in seabed:
                        seabed[pos] += 1
                    else:
                        seabed[pos] = 1
                    y += 1

            elif x1>x2 and y1>y2:
                print('diagonal -1,-1')
                y = y1
                for x in range(x1,x2-1,-1):
                    pos = (x,y)
                    if pos in seabed:
                        seabed[pos] += 1
                    else:
                        seabed[pos] = 1
                    y -= 1
            elif x1<x2 and y1>y2:
                print('diagonal 1,-1')
                y = y1
                for x in range(x1,x2+1):
                    pos = (x,y)
                    if pos in seabed:
                        seabed[pos] += 1
                    else:
                        seabed[pos] = 1
                    y -= 1
            elif x1>x2 and y1<y2:
                print('diagonal -1,1')
                y = y1
                for x in range(x1,x2-1,-1):
                    pos = (x,y)
                    if pos in seabed:
                        seabed[pos] += 1
                    else:
                        seabed[pos] = 1
                    y += 1



# print(seabed)
count = 0
for k,v in seabed.items():
    if seabed[k] > 1:
        count += 1

print(count)