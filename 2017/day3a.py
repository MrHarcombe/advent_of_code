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

print(manhattan_distance(spiral(277678), (0,0)))
