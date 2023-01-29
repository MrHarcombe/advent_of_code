test = '3,4,3,1,2'

import io

fishes = []
# with io.StringIO(test) as starting_population:
with open('input6.txt') as starting_population:
    fishes = starting_population.readline().split(',')

timers = []
for timer in range(9):
    timers.append(fishes.count(str(timer)))
print(timers)

##
# credit to Adam F for this solution - fabulous thinking !!
#
generations = 256 # 18 for example, 80 for live input, 256 for part 2
for generation in range(generations):
    breed = timers[0]
    new_timers = 9 * [0]
    for timer in range(8):
        new_timers[timer] = timers[timer+1]

    new_timers[6] += breed
    new_timers[8] += breed
    timers = new_timers
    # print(timers)

print(sum(timers))

##
# solution below is O(n**2) -- too inefficient for
# the size of the data set given and the number of generations
# used in part2
#
'''
generations = 256 # 18 for example, 80 for live input, 256 for part 2
current_generation = 0

while current_generation < generations:
    fishes = [n - 1 for n in fishes]

    new_fish = fishes.count(-1)
    fishes = [6 if n == -1 else n for n in fishes]
    fishes += new_fish * [8]

    current_generation += 1
    print(current_generation, len(fishes))

print(len(fishes))
'''
