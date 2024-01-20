from collections import defaultdict
from io import StringIO
from math import lcm
from time import time

# test = """broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a"""

test = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

LOW = 0
HIGH = 1

class module:
    high_pulse_count = 0
    low_pulse_count = 0
    
    def __init__(self, name, queue):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.pulse_queue = queue
        self.low_pulse_count = 0
        self.high_pulse_count = 0

    def register_publisher(self, pub):
        self.inputs.append(pub)

    def register_listener(self, sub):
        self.outputs.append(sub)
        sub.register_publisher(self)

    def _output(self, value):
        for s in self.outputs:
            if value == LOW:
                module.low_pulse_count += 1
            else:
                module.high_pulse_count += 1
            self.pulse_queue.append((self.name, s.name, value))
            # print("Pulsing:", (str(self), "LOW" if value == LOW else "HIGH", str(s)))

    def input(self, value):
        if self.name == "rx" and value == LOW:
            module.rx_low = True
        # print("Unexpected input to", self.name, "LOW" if value == LOW else "HIGH")

    def reset(self):
        pass

    def __str__(self):
        return f"{self.name}_{type(self).__name__}"

class broadcaster(module):
    def input(self, pulse):
        self._output(pulse[2])

class button(module):
    def __init__(self, name, queue):
        super().__init__(name, queue)
        self.button_presses = 0
        
    def output(self):
        self.button_presses += 1
        super()._output(LOW)

class flipflop(module):
    def __init__(self, name, queue):
        super().__init__(name, queue)
        self.state = False
        
    def input(self, pulse):
        src, dest, value = pulse
        if value == LOW:
            self.state = not self.state
            super()._output(HIGH if self.state else LOW)

    def reset(self):
        self.state = False

class conjunction(module):
    def __init__(self, name, queue):
        super().__init__(name, queue)
        self.previous = defaultdict(lambda: LOW)

    def input(self, pulse):
        src, dest, value = pulse
        self.previous[src] = value
        
        if value == LOW:
            self.low_pulse_count += 1
        else:
            self.high_pulse_count += 1

        super()._output(LOW if all(self.previous[n.name] == HIGH for n in self.inputs) else HIGH)

    def reset(self):
        self.previous = defaultdict(lambda: LOW)


pulse_queue = []
modules = {"output" : module("output", pulse_queue)}

module_list = []
# with StringIO(test) as data:
with open("input20.txt") as data:
    for line in data:
        modul, destinations = line.strip().split(" -> ")
        module_list.append((modul, destinations))
        if modul[0] == "%":
            modules[modul[1:]] = flipflop(modul[1:], pulse_queue)
        elif modul[0] == "&":
            modules[modul[1:]] = conjunction(modul[1:], pulse_queue)
        else:
            modules[modul] = broadcaster(modul, pulse_queue)
            
    for modul, destinations in module_list:
        name = modul
        if modul[0] in ("%","&"):
            name = modul[1:]
        for destination in destinations.split(","):
            if destination not in modules:
                modules[destination] = module(destination, pulse_queue)
            modules[name].register_listener(modules[destination.strip()])

begin = time()
start = button("start", pulse_queue)
start.register_listener(modules["broadcaster"])

for _ in range(1000):
    start.output()
    while len(pulse_queue) > 0:
        pulse = pulse_queue.pop(0)
        modules[pulse[1]].input(pulse)

print("Part 1:", module.low_pulse_count * module.high_pulse_count)
print("Elapsed:", time() - begin)

with open("day20-machine.dot", "w") as dot:
    print("graph {", file=dot)
    print("edge [colorscheme=spectral10];", file=dot)
    print("layout=neato;", file=dot)
    edge = 0

    visited = set()
    queue = [start]
    while len(queue) > 0:
        current = queue.pop(0)
        if current not in visited:
            visited.add(current)
            for o in current.outputs:
                # print(n, "--", "{", " ".join(nc for (nc, _) in connections.get_connections(n)), "}", file=dot)
                edge += 1
                print(current, "--", o, f'[color={edge%10}, tooltip="{current} to {o}"];', file=dot)
                queue.append(o)
    print("}", file=dot)

print("Dot file created")

parts = []
for _ in range(4):
    m1 = input("Top branch flip-flip: ")
    m2 = input("Bottom branch conjunction: ")

    for m in modules.values():
        m.reset()
    
    begin = time()
    start = button("start", pulse_queue)
    start.register_listener(modules[m1])

    while modules[m2].low_pulse_count == 0:
        start.output()
        while len(pulse_queue) > 0:
            pulse = pulse_queue.pop(0)
            modules[pulse[1]].input(pulse)

    parts.append(start.button_presses)

print("Part 2:", lcm(*parts))
print("Elapsed:", time() - begin)
