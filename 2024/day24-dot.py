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

# with StringIO(test) as input_data:
with open("input24.txt") as input_data:
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

with open("day24.dot", "w") as file:
    print("graph {", file=file)
    for gate in gates.values():
        if isinstance(gate, ConstanteGate):
            print(f'{gate.name} [shape="point", xlabel={gate.get_value()}]', file=file)

        elif isinstance(gate, AndGate):
            print(f'{gate.name} -- {gate.input1} [shape="diamond"]', file=file)
            print(f'{gate.name} -- {gate.input2} [shape="diamond"]', file=file)

        elif isinstance(gate, OrGate):
            print(f'{gate.name} -- {gate.input1} [shape="circle"]', file=file)
            print(f'{gate.name} -- {gate.input2} [shape="circle"]', file=file)

        elif isinstance(gate, XorGate):
            print(f'{gate.name} -- {gate.input1} [shape="doublecircle"]', file=file)
            print(f'{gate.name} -- {gate.input2} [shape="doublecircle"]', file=file)
    print("}", file=file)
