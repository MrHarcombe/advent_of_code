from io import StringIO

triggers = ("^^.", ".^^", "^..", "..^")

def generate_square(above):
    if above in triggers:
        return "^"
    return "."

def generate_row(previous_row):
    #print(previous_row)
    next_row = []
    for i in range(len(previous_row)):
        if i == 0:
            #print("first: ." + previous_row[i:i+2])
            next_row.append(generate_square("." + previous_row[i:i+2]))
        elif i == len(previous_row)-1:
            #print("last:", previous_row[i-1:i+1] + ".")
            next_row.append(generate_square(previous_row[i-1:i+1] + "."))
        else:
            #print("mid:", previous_row[i-1:i+2])
            next_row.append(generate_square(previous_row[i-1:i+2]))
            
    return "".join(next_row)

test = "..^^."
test = ".^^.^.^^^^"
actual = "...^^^^^..^...^...^^^^^^...^.^^^.^.^.^^.^^^.....^.^^^...^^^^^^.....^.^^...^^^^^...^.^^^.^^......^^^^"

rows = []
print(actual)
row = actual
rows.append(row)
while len(rows) < 400000:
    row = generate_row(row)
    rows.append(row)
    #print(row)
print(sum([sum([1 for ch in row if ch == '.']) for row in rows]))
