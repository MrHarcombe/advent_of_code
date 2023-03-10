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

# with StringIO(test) as data:
with open("input13.txt") as data:
    for line in data:
        layer, depth = [int(n) for n in line.split(":")]
        #print(layer, depth)
        layers[layer] = depth

uncaught = True
delay = -1
probe = 0
while uncaught and probe <= max(layers.keys()):
    probe = 0
    severity = 0
    delay += 1
    
    for time in range(delay, delay + max(layers.keys()) + 1):
        # print("delay:", delay, "probe:", probe)
        for l in layers:
            # print("time:", time, "layer:", l, "at:", get_layer_value(l, time))
            if get_layer_value(l, time) == 0 and probe == l:
                uncaught = False
                break
        
        if not uncaught:
            uncaught = True
            break
        
        probe += 1

print("Delay:", delay, "Severity:", severity)
