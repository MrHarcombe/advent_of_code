from io import StringIO
from time import time


class CPU:
    def __init__(self, program, rA=0, rB=0, rC=0):
        self.program = program
        self.rA = rA
        self.rB = rB
        self.rC = rC
        self.IP = 0
        self.output = []

    def has_finished(self):
        return self.IP >= len(self.program)

    def get_output(self):
        return ",".join(self.output)

    def resolve_combo(self, operand):
        if operand < 4:
            return operand
        elif operand == 4:
            return self.rA
        elif operand == 5:
            return self.rB
        elif operand == 6:
            return self.rC
        else:
            print("Uh-oh (combo operand):", operand)
            return 7

    def tick(self):
        opcode = self.program[self.IP]
        operand = self.program[self.IP + 1]
        jumped = False

        match opcode:
            case 0:
                numerator = self.rA
                denominator = 2 ** self.resolve_combo(operand)
                self.rA = numerator // denominator

            case 1:
                self.rB = self.rB ^ operand

            case 2:
                self.rB = self.resolve_combo(operand) % 8

            case 3:
                if self.rA != 0:
                    jumped = True
                    self.IP = operand

            case 4:
                self.rB = self.rB ^ self.rC

            case 5:
                self.output.append(str(self.resolve_combo(operand) % 8))

            case 6:
                numerator = self.rA
                denominator = 2 ** self.resolve_combo(operand)
                self.rB = numerator // denominator

            case 7:
                numerator = self.rA
                denominator = 2 ** self.resolve_combo(operand)
                self.rC = numerator // denominator

        if not jumped:
            self.IP += 2


test = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

test = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


# with StringIO(test) as input_data:
with open("input17.txt") as input_data:
    rA, rB, rC = 0, 0, 0
    program = None
    for line in input_data:
        if "A:" in line.strip():
            rA = int(line.strip().split()[-1])
        elif "B:" in line.strip():
            rB = int(line.strip().split()[-1])
        elif "C:" in line.strip():
            rC = int(line.strip().split()[-1])
        elif "Program:" in line.strip():
            program = line.strip().split()[-1]

begin = time()
cpu = CPU(list(map(int, program.split(","))), rA, rB, rC)
while not cpu.has_finished():
    cpu.tick()

print("Part 1:", cpu.get_output())
print("Elapsed:", time() - begin)

# new_rA = 0
# not_found = True
# while not_found:
#     new_rA += 1
#     cpu = CPU(list(map(int, program.split(","))), new_rA, rB, rC)
#     while not cpu.has_finished():
#         cpu.tick()

#         if len(cpu.get_output()) == 0:
#             continue

#         else:
#             if cpu.get_output() == program:
#                 not_found = False
#                 break
#             elif program.startswith(cpu.get_output()):
#                 continue
#             else:
#                 if new_rA % 100_000 == 0:
#                     print("new_rA:", new_rA)
#                 break

# print("Part 2:", new_rA, "->", cpu.get_output())
