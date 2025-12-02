from collections import defaultdict
from io import StringIO

test = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/"""

test = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""


DIRECTIONS = "^>v<"
MOVEMENT = { "^": complex(0,-1), ">": complex(1,0), "v": complex(0,1), "<": complex(-1,0) }
TURNS = (-1, 0, 1)

def display_tracks(carts, tracks):
    min_x = int(min(tracks, key=lambda t: t.real).real)
    max_x = int(max(tracks, key=lambda t: t.real).real)
    min_y = int(min(tracks, key=lambda t: t.imag).imag)
    max_y = int(max(tracks, key=lambda t: t.imag).imag)
    
    for y in range(min_y, max_y+1):
        row = []
        for x in range(min_x, max_x+1):
            location = complex(x,y)
            if location in carts:
                cart = carts[location]
                if type(cart) == tuple:
                    row.append(cart[0])
                else:
                    row.append(cart)
            elif location in tracks:
                row.append(tracks[location])
            else:
                row.append(" ")
        print("".join(row))
    print()

def get_carts(carts):
    for k in sorted(carts, key=lambda c: (c.imag,c.real)):
        yield k

def process_cart_move(cart, carts, tracks, delete_crashes=False):
    if cart not in carts:
        # previously crashed and removed
        return
    
    current_direction, intersection_count = carts[cart]

    next_position = cart + MOVEMENT[current_direction]
    next_direction = current_direction
    
    if next_position in carts:
        # collision
        del carts[cart]
        if delete_crashes:
            del carts[next_position]
        else:
            carts[next_position] = "X"
    
    else:
        if tracks[next_position] == "+":
            turn_effect = TURNS[intersection_count % len(TURNS)]
            next_direction = DIRECTIONS[(DIRECTIONS.index(current_direction) + turn_effect) % len(DIRECTIONS)]
            intersection_count += 1

        elif tracks[next_position] in ("\\", "/"):
            match current_direction:
                case "^":
                    if tracks[next_position] == "/":
                        next_direction = ">"
                    else:
                        next_direction = "<"
                case "v":
                    if tracks[next_position] == "/":
                        next_direction = "<"
                    else:
                        next_direction = ">"
                case "<":
                    if tracks[next_position] == "/":
                        next_direction = "v"
                    else:
                        next_direction = "^"
                case ">":
                    if tracks[next_position] == "/":
                        next_direction = "^"
                    else:
                        next_direction = "v"

        del carts[cart]
        carts[next_position] = (next_direction, intersection_count)

def part1(carts, tracks):
    crashed = False
    while not crashed:
        # display_tracks(carts, tracks)
        # input("> ")
        for cart in get_carts(carts):
            if crashed: break
            process_cart_move(cart, carts, tracks)
            crashed = "X" in carts.values()

    crash_location = [c for c in carts.items() if carts[c[0]] == "X"]
    return crash_location[0][0]

def part2(carts, tracks):
    while len(carts) > 1:
        # display_tracks(carts, tracks)
        # input("> ")
        for cart in get_carts(carts):
            process_cart_move(cart, carts, tracks, True)

    final_location = [c for c in carts.items()]
    return final_location[0][0]

tracks = defaultdict(lambda:" ")
carts = {}

# with StringIO(test) as data:
with open("input13.txt") as data:
    for y, line in enumerate(data):
        for x, ch in enumerate(line.rstrip()):
            match ch:
                case "-":
                    tracks[complex(x,y)] = "-"
                    
                case "|":
                    tracks[complex(x,y)] = "|"
                    
                case "/":
                    tracks[complex(x,y)] = "/"
                    
                case "\\":
                    tracks[complex(x,y)] = "\\"

                case "+":
                    tracks[complex(x,y)] = "+"

                case "^":
                    tracks[complex(x,y)] = "|"
                    carts[complex(x,y)] = ("^", 0)
                    
                case "v":
                    tracks[complex(x,y)] = "|"
                    carts[complex(x,y)] = ("v", 0)

                case "<":
                    tracks[complex(x,y)] = "-"
                    carts[complex(x,y)] = ("<", 0)

                case ">":
                    tracks[complex(x,y)] = "-"
                    carts[complex(x,y)] = (">", 0)

print("Part 1:", part1(dict(carts), tracks))
print("Part 2:", part2(dict(carts), tracks))
