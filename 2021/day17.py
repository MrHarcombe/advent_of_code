import io


def affect_velocity(v):
    x, y = v
    if x > 0:
        x -= 1
    elif x < 0:
        x += 1
    
    y -= 1

    return (x,y)


test = 'target area: x=20..30, y=-10..-5'

seabed = {}

with io.StringIO(test) as inputs:
    target_input = inputs.readline().strip()
    values = target_input.split(':')[1]
    x_part, y_part = values.split(', ')
    x_range = [int(n) for n in x_part.split('=')[1].split('..')]
    y_range = [int(n) for n in y_part.split('=')[1].split('..')]

    min_x, max_x = min(x_range), max(x_range)
    min_y, max_y = min(y_range), max(y_range)

    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            seabed[(x,y)] = 'T'

print(seabed)
current = (0,0)
