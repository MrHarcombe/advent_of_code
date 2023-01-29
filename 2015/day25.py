##
# To continue, please consult the code grid in the manual.  Enter the code at row 2981, column 3075.
#

row = 2981
col = 3075

# col = 1
# row = 2

row_start = ((row ** 2 - row) // 2) + 1
sequence = row_start
inc = row
for n in range(col-1):
    inc += 1
    sequence += inc

print(sequence)

value = 20151125
for i in range(sequence-1):
    value *= 252533
    value %= 33554393

print(value)
