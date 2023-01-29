import io


def parse_binary_stream(stream):
    position = 0
    pversion = stream[position:position+3]
    ptype = stream[position+3:position+6]
    position += 6
    pdata = None

    if ptype == '100':
        pdata = []
        while stream[position] == '1':
            pdata.append(stream[position+1:position+5])
            position += 5
        pdata.append(stream[position+1:position+5])
        position += 5
    else:
        length_id = stream[position]
        position += 1
        if length_id == '0':
            packet_length = stream[position:position+14]
            # print(stream[position:])
            # print('packet_length:', packet_length)
            position += 15
        else:
            packet_count = stream[position:position+11]
            position += 11

    return pversion, ptype, stream[position:]


def decode_literal(pdata):
    pvalue = ''.join(pdata)
    value = int(pvalue, 2)
    return value

test_1 = '''D2FE28'''
test_2 = '''38006F45291200'''
test_3 = '''8A004A801A8002F478'''
test_4 = '''620080001611562C8802118E34'''
test_5 = '''C0015000016115A2E0802F182340'''
test_6 = '''A0016C880162017C3686B18A3D4780'''

test = test_6

binary_stream = ''
# with io.StringIO(test) as inputs:
with open('input16.txt') as inputs:
    for line in inputs:
        for ch in line.strip():
            value = int(ch, 16)
            binary_stream += f'{value:04b}'

print(binary_stream)

position = 0
version_sum = 0
packet_version, packet_type, packet_data = parse_binary_stream(binary_stream)
print(packet_version,packet_type, len(packet_data))
version_sum += int(packet_version,2)
while len(packet_data) > 6:
    packet_version, packet_type, packet_data = parse_binary_stream(packet_data)
    print(packet_version,packet_type, len(packet_data))
    version_sum += int(packet_version,2)

print(version_sum)