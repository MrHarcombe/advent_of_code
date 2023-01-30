from math import ceil

## from https://math.stackexchange.com/a/163101
# 
# function spiral(n)
#         k=ceil((sqrt(n)-1)/2)
#         t=2*k+1
#         m=t^2 
#         t=t-1
#         if n>=m-t then return k-(m-n),-k        else m=m-t end
#         if n>=m-t then return -k,-k+(m-n)       else m=m-t end
#         if n>=m-t then return -k+(m-n),k else return k,k-(m-n-t) end
# end

def spiral(n):
    k = ceil(((n ** 0.5) - 1) / 2)
    t = 2 * k + 1
    m = t ** 2
    t = t - 1
    
    if n >= m - t:
        return (k - (m - n), -k)
    else:
        m -= t
    
    if n >= m - t:
        return (-k, -k + (m-n))
    else:
        m -= t
        
    if n >= m - t:
        return (-k + (m-n), k)
    else:
        return (k, k - (m - n - t))

def manhattan_distance(pa, pb):
    return sum((abs(a - b) for a,b in zip(pa, pb)))

def get_neighbours(cell):
    neighbours = []
    for dx,dy in ((-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1)):
        neighbours.append((cell[0]+dx, cell[1]+dy))
    return neighbours

target_square = 277678

# print(manhattan_distance(spiral(target_square), (0,0)))

square = 1
value = 1
values = { spiral(1): 1 }
while value < target_square:
    square += 1
    value = 0
    for n in get_neighbours(spiral(square)):
        if n in values:
            value += values[n]
    values[spiral(square)] = value
    # print(square, spiral(square), "->", value)

print(square, value)
