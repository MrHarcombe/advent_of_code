from functools import cache
from io import StringIO
from itertools import combinations, product

test = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

def patterns(coeffs: list[tuple[int, ...]]) -> dict[tuple[int, ...], dict[tuple[int, ...], int]]:
    num_buttons = len(coeffs)
    num_variables = len(coeffs[0])
    # build an empty dictionary of dictionaries for each of the possible button bit patterns
    out = {parity_pattern: {} for parity_pattern in product(range(2), repeat=num_variables)}
    for num_pressed_buttons in range(num_buttons+1):
        # build up a map of the parity pattern
        #            against (each pattern against total count of buttons pressed)
        for buttons in combinations(range(num_buttons), num_pressed_buttons):
            pattern = tuple(map(sum, zip((0,) * num_variables, *(coeffs[i] for i in buttons))))
            parity_pattern = tuple(i%2 for i in pattern)
            if pattern not in out[parity_pattern]:
                out[parity_pattern][pattern] = num_pressed_buttons
    
    # final dictionary contains all of the costs of all possible patterns (ie combinations) of
    # button presses (whether good or bad) keyed by the parity pattern
    return out

def solve_single(coeffs: list[tuple[int, ...]], goal: tuple[int, ...]) -> int:
    pattern_costs = patterns(coeffs)
    @cache
    def solve_single_aux(goal: tuple[int, ...]) -> int:
        # catch the empty case
        if all(i == 0 for i in goal): return 0
        # work down to the best answer
        answer = float("inf")
        # consider each of the prepared pattern against costs, looking by pattern parity
        for pattern, pattern_cost in pattern_costs[tuple(i%2 for i in goal)].items():
            # recurse down, taking the number of presses down each time
            if all(i <= j for i, j in zip(pattern, goal)):
                # but search by halves, doubling up the cost from here
                new_goal = tuple((j - i)//2 for i, j in zip(pattern, goal))
                answer = min(answer, pattern_cost + 2 * solve_single_aux(new_goal))
        return answer
    return solve_single_aux(goal)

def solve(raw: str):
    score = 0
    lines = raw.splitlines()
    for count, line in enumerate(lines, 1):
        # don't need the pattern, just the button combinations and the goal (button counts)
        _, *coeff_str, goal = line.split()
        # split the goal into a tuple of ints
        goal = tuple(int(i) for i in goal[1:-1].split(","))
        # split the coefficients into a list of lists (of the buttons)
        buttons = [[int(i) for i in r[1:-1].split(",")] for r in coeff_str]
        # split further into the final list of tuples (of bit patterns)
        coeffs = [tuple(int(i in r) for i in range(len(goal))) for r in buttons]

        # solve each in turn, keeping a tally
        subscore = solve_single(coeffs, goal)
        # print(f'Line {count}/{len(lines)}: answer {subscore}')
        score += subscore
    print(score)

# solve(StringIO(test).read())
solve(open("input10.txt").read())
