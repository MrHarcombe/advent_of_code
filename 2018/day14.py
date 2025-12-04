from time import time

recipes = [3,7]
elves = [0,1]

target = 637061

def part1(recipes, elves, target):
    while len(recipes) < target + 10:
        new_recipe = sum(recipes[elf] for elf in elves)
        for digit in str(new_recipe):
            recipes.append(int(digit))

        for i_elf, elf in enumerate(elves):
            new_elf = (elves[i_elf] + recipes[elf] + 1) % len(recipes)
            elves[i_elf] = new_elf
            
    return "".join(map(str, recipes[target:target+10]))


def part2(recipes, elves, target):
    target_list = list(map(int, str(target)))

    # Source - https://stackoverflow.com/questions/7100242/python-numpy-first-occurrence-of-subarray
    # Posted by norok2, modified by community. See post 'Timeline' for change history
    # Retrieved 2025-12-04, License - CC BY-SA 4.0

    def find_mix2(seq, subseq):
        n = len(seq)
        m = len(subseq)
        for i in range(n - m + 1):
            if seq[i] == subseq[0] and seq[i + m - 1] == subseq[m - 1] and seq[i:i + m] == subseq:
                return i
        return -1

    index = -1
    block = 0
    while index == -1:
        block += 7_500_000
        while len(recipes) < block:
            new_recipe = sum(recipes[elf] for elf in elves)
            for digit in str(new_recipe):
                recipes.append(int(digit))

            for i_elf, elf in enumerate(elves):
                new_elf = (elves[i_elf] + recipes[elf] + 1) % len(recipes)
                elves[i_elf] = new_elf
            
        index = find_mix2(recipes, target_list)
        print(f"Recipes length: {len(recipes):n} and index=", index)
            
    return index

print("Part 1:", part1([3,7], [0,1], target))
begin = time()
print("Part 2:", part2([3,7], [0,1], target))
print("Elapsed:", time() - begin)
