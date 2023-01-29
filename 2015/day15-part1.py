test = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''

import io

ingredients = {}

#with io.StringIO(test) as ingredient_file:
with open('input.txt') as ingredient_file:
    for ingredient_line in ingredient_file:
        ingredient, details = ingredient_line.strip().split(':')
        ingredients[ingredient] = [int(n.split()[1]) for n in details.split(',')]

print(ingredients)

ingredient_list = list(ingredients.keys())

import itertools
high_score = 0
for quantities in itertools.product(range(1,100),repeat=len(ingredients.keys())):
    if sum(quantities) == 100:
        total_calories = 0
        for i in range(len(quantities)):
            total_calories += ingredients[ingredient_list[i]][-1] * quantities[i]

        if total_calories == 500:
            total_score = 1
            for qualities in range(4):
                score = 0
                for i in range(len(quantities)):
                    ingredient = ingredient_list[i]
                    quantity = quantities[i]
                    quality = ingredients[ingredient][qualities]
                    score += quantity * quality
                if score < 0:
                    score = 0
                total_score *= score
            if total_score > high_score:
                high_score = total_score

print(high_score)