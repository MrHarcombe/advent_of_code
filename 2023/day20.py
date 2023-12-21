from collections import defaultdict
from io import StringIO

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
    button_presses = 0
    rx_low = False
    
    def __init__(self, name, queue):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.pulse_queue = queue

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
            module.rx_low = Truw
        # print("Unexpected input to", self.name, "LOW" if value == LOW else "HIGH")

    def __str__(self):
        return f"{self.name}({type(self).__name__})"

class broadcaster(module):
    def input(self, pulse):
        module.button_presses += 1
        self._output(pulse[2])

class button(module):
    def output(self):
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
            
class conjunction(module):
    def __init__(self, name, queue):
        super().__init__(name, queue)
        self.previous = defaultdict(lambda: LOW)

    def input(self, pulse):
        src, dest, value = pulse
        self.previous[src] = value
        # print(self.name, [str(i) for i in self.inputs], self.previous)
        super()._output(LOW if all(self.previous[n.name] == HIGH for n in self.inputs) else HIGH)
        # output = LOW
        # for n in self.inputs:
        #     if self.previous[n.name] == LOW:
        #         output = HIGH
        # super()._output(output)


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

start = button("start", pulse_queue)
start.register_listener(modules["broadcaster"])

while not module.rx_low:
    start.output()
    while len(pulse_queue) > 0:
        pulse = pulse_queue.pop(0)
        modules[pulse[1]].input(pulse)

# print("Part 1:", module.low_pulse_count * module.high_pulse_count)
print("Part 2:", module.button_presses)
