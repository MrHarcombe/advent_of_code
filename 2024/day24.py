from io import StringIO
from itertools import combinations

test = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

test = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""


class Gate:
    def __init__(self, name):
        self.name = name

    def is_resolved(self):
        return False


class ConstanteGate(Gate):
    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

    def is_resolved(self):
        return True

    def get_value(self):
        return self.value


class OperationGate(Gate):
    def __init__(self, name, input1, input2):
        super().__init__(name)
        self.input1 = input1
        self.input2 = input2

    def is_resolved(self):
        return type(self.input1) != str and type(self.input2) != str


class AndGate(OperationGate):
    def __init__(self, name, input1, input2):
        super().__init__(name, input1, input2)

    def get_value(self):
        return (
            "1"
            if all(i.get_value() == "1" for i in (self.input1, self.input2))
            else "0"
        )


class OrGate(OperationGate):
    def __init__(self, name, input1, input2):
        super().__init__(name, input1, input2)

    def get_value(self):
        return (
            "1"
            if any(i.get_value() == "1" for i in (self.input1, self.input2))
            else "0"
        )


class XorGate(OperationGate):
    def __init__(self, name, input1, input2):
        super().__init__(name, input1, input2)

    def get_value(self):
        return "1" if self.input1.get_value() != self.input2.get_value() else "0"


def get_int_value(prefix):
    return int(
        "".join(
            [
                gv.get_value()
                for gk, gv in sorted(gates.items(), reverse=True)
                if gk[0] == prefix
            ]
        ),
        2,
    )


gates = {}
z_gates = []

# with StringIO(test) as input_data:
with open("input24-fix.txt") as input_data:
    for line in input_data:
        if ":" in line:
            name, value = line.strip().split(": ")
            gates[name] = ConstanteGate(name, value)

        elif " -> " in line:
            ops, name = line.strip().split(" -> ")
            input1, op, input2 = ops.split()
            if op == "AND":
                gates[name] = AndGate(name, input1, input2)
            elif op == "OR":
                gates[name] = OrGate(name, input1, input2)
            elif op == "XOR":
                gates[name] = XorGate(name, input1, input2)

        if name[0] == "z":
            z_gates.append(gates[name])

# print(gates)
# print(z_gates)

all_resolved = False
while not all_resolved:
    all_resolved = True
    for gate in gates:
        if not gates[gate].is_resolved():
            g1 = gates[gates[gate].input1]
            g2 = gates[gates[gate].input2]

            gates[gate].input1 = g1
            gates[gate].input2 = g2

            if g1 is None or g2 is None:
                all_resolved = False

print(
    "Part 1:",
    int(
        "".join(
            [
                g.get_value()
                for g in sorted(z_gates, key=lambda item: item.name, reverse=True)
            ]
        ),
        2,
    ),
)

goal_total = get_int_value("x") + get_int_value("y")

print("x=", get_int_value("x"))
print("y=", get_int_value("y"))
print("so should=", goal_total)

carry_gate = ""
for bit in range(len(z_gates) - 1):
    xbit = f"x{bit:02}"
    ybit = f"y{bit:02}"

    xbits = {
        k
        for k, v in gates.items()
        if isinstance(v, OperationGate)
        and (v.input1.name == xbit or v.input2.name == xbit)
    }
    ybits = {
        k
        for k, v in gates.items()
        if isinstance(v, OperationGate)
        and (v.input1.name == ybit or v.input2.name == ybit)
    }

    if xbits != ybits:
        print("Problem on bit", bit)
        print(f"x{bit:02}", xbits)
        print(f"y{bit:02}", ybits)
    # else:
    #     print("Bit:", bit, xbits, "==", ybits)

    # now only using xbits, as xbits and ybits go to the same places - just checked that

    if bit == 0:
        g1, g2 = xbits
        if (g1 != "z00" or not isinstance(gates[g2], AndGate)) and (
            g2 != "z00" or not isinstance(gates[g1], AndGate)
        ):
            print("Problem with bit 0:", g1, type(gates[g1]), g2, type(gates[g2]))
        else:
            carry_gate = g2 if g1 == "z00" else g1

        print("z00", carry_gate)

    else:
        g1, g2 = xbits

        h1_xor = g1 if isinstance(gates[g1], XorGate) else g2
        h1_and = g2 if h1_xor == g1 else g1

        h2_xor = {
            k
            for k, v in gates.items()
            if isinstance(v, XorGate)
            and (
                (v.input1.name == h1_xor or v.input2.name == h1_xor)
                and (
                    carry_gate is None
                    or v.input1.name == carry_gate
                    or v.input2.name == carry_gate
                )
            )
        }

        h2_and = {
            k
            for k, v in gates.items()
            if isinstance(v, AndGate)
            and (
                (v.input1.name == h1_xor or v.input2.name == h1_xor)
                and (
                    carry_gate is None
                    or v.input1.name == carry_gate
                    or v.input2.name == carry_gate
                )
            )
        }

        h2_carry = {
            k
            for k, v in gates.items()
            if isinstance(v, OrGate)
            and (
                (v.input1.name == h1_and or v.input2.name == h1_and)
                and (v.input1.name in h2_and or v.input2.name in h2_and)
            )
        }

        print(bit, h1_xor, h1_and, h2_xor, h2_and, h2_carry)

        # if (g1 != f"z{bit:02}" or not isinstance(gates[g2], OrGate)) and (
        #     g2 != f"z{bit:02}" or not isinstance(gates[g1], OrGate)
        # ):
        #     print(f"Problem with bit {bit}:", g1, type(gates[g1]), g2, type(gates[g2]))

        if len(h2_carry) > 0:
            carry_gate = next(iter(h2_carry))
        else:
            carry_gate = None

changes = ["z07", "shj", "wkb", "tpk", "z23", "pfn", "z27", "kcd"]

print("Part 2:", ",".join(sorted(changes)))

# swappable_gates = list(filter(lambda name: name[0] not in ("x", "y"), gates.keys()))
# for swap_these in combinations(swappable_gates, 8):
#     for gate in gates.values():
#         if isinstance(gate, OperationGate):
#             for i in range(0, len(swap_these), 2):
#                 if gate.input1 == swap_these[i]:
#                     gate.input1 == swap_these[i + 1]
#                 elif gate.input1 == swap_these[i + 1]:
#                     gate.input1 == swap_these[i]

#                 if gate.input2 == swap_these[i]:
#                     gate.input2 == swap_these[i + 1]
#                 elif gate.input2 == swap_these[i + 1]:
#                     gate.input2 == swap_these[i]

#             new_z = get_int_value("z")
#             if new_z == goal_total:
#                 print(",".join(sorted(swap_these)))
#                 exit(0)

#             for i in range(0, len(swap_these), 2):
#                 if gate.input1 == swap_these[i]:
#                     gate.input1 == swap_these[i + 1]
#                 elif gate.input1 == swap_these[i + 1]:
#                     gate.input1 == swap_these[i]

#                 if gate.input2 == swap_these[i]:
#                     gate.input2 == swap_these[i + 1]
#                 elif gate.input2 == swap_these[i + 1]:
#                     gate.input2 == swap_these[i]
