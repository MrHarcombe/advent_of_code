from io import StringIO
import numpy

# MAX_IP = 10
MAX_IP = 2**32

test = """5-8
0-2
4-7"""

a = numpy.full(MAX_IP, 1, numpy.bool_)
# print(len(a), a[0]) 
# print(numpy.count_nonzero(a))

# with StringIO(test) as f:
with open("input20.txt") as f:
    for line in f:
        low,high = [int(n) for n in line.split("-")]
        a[low:high+1] = 0
        
print(min(numpy.where(a == True)[0]))
print(numpy.count_nonzero(a))
