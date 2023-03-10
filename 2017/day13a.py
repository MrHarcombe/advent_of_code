from io import StringIO

test = """0: 3
1: 2
4: 4
6: 4"""

layers = {}

def get_layer_value(layer, time):
    # modified from https://en.wikipedia.org/wiki/Triangle_wave
    amp = layers[layer] - 1
    per = 2 * amp
    
    return 2 * amp // per * abs(((time - per // 2) % per) - per // 2) # - amp

with StringIO(test) as data:
# with open("input13.txt") as data:
    for line in data:
        layer, depth = [int(n) for n in line.split(":")]
        #print(layer, depth)
        layers[layer] = depth

probe = 0
severity = 0
for time in range(max(layers.keys())+1):
    #print("probe:", probe)
    for l in layers:
        #print("time:", time, "layer:", l, "at:", get_layer_value(l, time))
        if get_layer_value(l, time) == 0 and probe == l:
            severity += l * layers[l]
    
    probe += 1

print("Severity:", severity)
