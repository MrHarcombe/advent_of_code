import io

test = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''

coords = {}
folds = []

# with io.StringIO(test) as inputs:
with open('input13.txt') as inputs:
    for line in inputs:
        if len(line.strip()) == 0:
            break
        x,y = [int(n) for n in line.split(',')]
        coords[(x,y)] = '#'

    for line in inputs:
        parts = line.strip().split()
        axis,number = parts[-1].split('=')
        folds.append((axis,int(number)))


def display_map(coords):
    max_x = 0
    max_y = 0
    for x, y in coords:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    output='\n'
    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x,y) in coords:
                output += '#'
            else:
                output += ' '
        output += '\n'
    return output


# print('size:', len(coords), display_map(coords))
print('size:', len(coords))
print('commands:', folds)

for axis, number in folds:
    new_coords = {}
    for x,y in coords:
        if axis == 'x':
            if x > number:
                x = number - abs(x - number)
            new_coords[(x,y)] = '#'
        elif axis == 'y':
            if y > number:
                y = number - abs(y - number)
            new_coords[(x,y)] = '#'
    coords = new_coords

# print('size:', len(coords), display_map(coords))
print('size:', len(coords))
print(display_map(coords))
with open('output13.txt', 'w') as file:
    file.write(display_map(coords))
