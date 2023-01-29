from collections import defaultdict
import io

test_1 = '''inp x
mul x -1'''
test_2 = '''inp z
inp x
mul z 3
eql z x'''
test_3 = '''inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2'''

test_i1 = '''inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y'''
test_i2 = '''inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y'''


test = test_i2
#                              11111
#                     12345678901234
largest_monad_model = 76543198765432
this_input = str(largest_monad_model)


def get_next_input():
    global this_input

    first = this_input[0]
    this_input = this_input[1:]
    return int(first)


def alu_execute(command, registers):
    operator = command.pop(0)

    if operator == 'inp':
        # for reg in ('w', 'x', 'y', 'z'):
        #     print(f'registers[{reg}]={registers[reg]}', end=' ')
        # print()
        a, = command
        registers[a] = get_next_input()

    elif operator == 'add':
        a, b = command
        b = registers[b] if b.isalpha() else int(b)
        registers[a] += b

    elif operator == 'mul':
        a, b = command
        b = registers[b] if b.isalpha() else int(b)
        registers[a] *= b

    elif operator == 'div':
        a, b = command
        b = registers[b] if b.isalpha() else int(b)
        registers[a] //= b

    elif operator == 'mod':
        a, b = command
        b = registers[b] if b.isalpha() else int(b)
        registers[a] %= b

    elif operator == 'eql':
        a, b = command
        b = registers[b] if b.isalpha() else int(b)
        registers[a] = (1 if registers[a] == b else 0)


commands = []

# with io.StringIO(test) as inputs:
with open('input24.txt') as inputs:
    commands = inputs.readlines()

this_input = '99959893326999'
registers = defaultdict(int)
registers['w'] = 0
registers['x'] = 0
registers['y'] = 0
registers['z'] = 0
for command in commands:
    alu_execute(command.strip().split(), registers)

print(this_input, '->', registers)

# while largest_monad_model > 10000000000000:
#     this_input = str(largest_monad_model)
#     registers = defaultdict(int)
#     for command in commands:
#         alu_execute(command.strip().split(), registers)

#     # print(registers)
#     if registers['z'] == 0:
#         print(largest_monad_model)
#         break
#     else:
#         print(largest_monad_model, '->', registers['z'])
#         largest_monad_model -= 1
#         while '0' in str(largest_monad_model):
#             largest_monad_model -= 1
