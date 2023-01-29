def whittle_down(input_list, most_bit, least_bit):
    loop_inputs = list(input_list)
    bit = 0
    while len(loop_inputs) > 1:
        if bit < len(loop_inputs[0]):
            loop_bits = [inp[bit] for inp in loop_inputs]
            loop_bit = most_bit if loop_bits.count("1") - loop_bits.count("0") >= 0 else least_bit

            loop_outputs = [inp for inp in loop_inputs if inp[bit] == loop_bit]
        loop_inputs = loop_outputs
        bit += 1

    return loop_inputs[0]

inputs = []

with open("input3.txt") as file:
    for line in file:
        inputs.append(line.strip())

most_input = whittle_down(inputs, "1", "0")
print(most_input)
generator = int(most_input, 2)

least_input = whittle_down(inputs, "0", "1")
print(least_input)
scrubber = int(least_input, 2)

print(generator * scrubber)
