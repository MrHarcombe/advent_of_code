import io
from math import prod
import operator


def parse_binary_stream(stream):
    position = 0
    _ = stream[position:position+3] # version
    ptype = stream[position+3:position+6]
    position += 6

    if ptype == '100':
        pdata = []

        while stream[position] == '1':
            pdata.append(stream[position+1:position+5])
            position += 5

        pdata.append(stream[position+1:position+5])
        position += 5
        return decode_literal(pdata), stream[position:]

    else:
        length_id = stream[position]
        position += 1
        if length_id == '0':
            packet_length = stream[position:position+15]
            # print(stream[position:])
            # print('packet_length:', packet_length)
            position += 15

            packets = []
            substream = stream[position:]
            target = len(substream) - int(packet_length, 2)
            while len(substream) > target:
                packet, substream = parse_binary_stream(substream)
                packets.append(packet)

        else:
            packet_count = stream[position:position+11]
            position += 11

            packets = []
            substream = stream[position:]
            for _ in range(int(packet_count,2)):
                packet, substream = parse_binary_stream(substream)
                packets.append(packet)

        if ptype == '000':
            return sum(packets), substream
        elif ptype == '001':
            return prod(packets), substream
        elif ptype == '010':
            return min(packets), substream
        elif ptype == '011':
            return max(packets), substream
        elif ptype == '101':
            return 1 if packets[0] > packets[1] else 0, substream
        elif ptype == '110':
            return 1 if packets[0] < packets[1] else 0, substream
        elif ptype == '111':
            return 1 if packets[0] == packets[1] else 0, substream


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

test_7 = 'C200B40A82'
test_8 = '04005AC33890'
test_9 = '880086C3E88112'
test_10 = 'CE00C43D881120'
test_11 = 'D8005AC2A8F0'
test_12 = 'F600BC2D8F'
test_13 = '9C005AC2F8F0'
test_14 = '9C0141080250320F1802104A08'

test = test_14

binary_stream = ''
# with io.StringIO(test) as inputs:
with open('input16.txt') as inputs:
    for line in inputs:
        for ch in line.strip():
            value = int(ch, 16)
            binary_stream += f'{value:04b}'

# print(binary_stream)

packets = []
packet_data = binary_stream
while len(packet_data) > 6:
    packet, packet_data = parse_binary_stream(packet_data)
    packets.append(packet)
    # print(packet, len(packet_data))

print(packets)