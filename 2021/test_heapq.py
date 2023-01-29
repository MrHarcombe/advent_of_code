from heapq import *

heap = []
heappush(heap, (1, 'fred'))
heappush(heap, (2, 'wilma'))
print(heap)

heappush(heap, (1, 'fred'))
print(heap)
print(nsmallest(2, heap))