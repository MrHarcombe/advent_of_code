from io import StringIO
import re

test = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

test = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

test = """eighthree
sevenine"""

p1pattern = re.compile(r'[0-9]')
p2pattern = re.compile(r'(?=([0-9])|(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine))')

values = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

part1 = 0
part2 = 0
# with StringIO(test) as data:
with open("input1.txt") as data:
    with open("trace1.txt", "w") as trace:
        for line in data:
            digits = p1pattern.findall(line)
            part1 += int(digits[0] + digits[-1])

            digits = [(m.start(), "".join(m.groups(""))) for m in p2pattern.finditer(line.strip())]
            d1 = digits[0][1] if digits[0][1].isdigit() else values[digits[0][1]]
            d2 = digits[-1][1] if digits[-1][1].isdigit() else values[digits[-1][1]]
            this_line = int(d1) * 10 + int(d2)
            part2 += this_line

print("Part 1:", part1)
print("Part 2:", part2)
