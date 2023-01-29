input_text = open('input14.txt', 'r')
lines = input_text.readlines()
starti = 0
endi = 600
startj = 0
endj = 250

coords = {}
for i in range(starti,endi):
    for j in range(startj,endj):
        coords[str(i)+'.'+str(j)] = 'e'

coords['500.0'] = '+'

def print_map():
    global starti
    global endi
    global startj
    global endj
    map_str = ''
    for i in range(startj,endj):
        map_str += '\n'
        for j in range(starti,endi-1):
            map_str += coords[str(j)+'.'+str(i)]

    print(map_str)

for line in lines:
    temp_line = (((line.strip()).replace(' ->','')).split(' '))
    temp_tuple = []
    for i in temp_line:
        temp_tuple.append(eval(i))
    for i in range(len(temp_tuple)):
        if i == len(temp_tuple)-1:
            None
        elif (temp_tuple[i])[0] == (temp_tuple[i+1])[0]:
            if temp_tuple[i][1] > temp_tuple[i+1][1]:
                temp_list = [temp_tuple[i][1]+1,(temp_tuple[i+1][1])]
            elif temp_tuple[i][1] < temp_tuple[i+1][1]:
                temp_list = [temp_tuple[i][1],(temp_tuple[i+1][1]+1)]
            for j in range(sorted(temp_list)[0],sorted(temp_list)[1]):
                coords[(str(temp_tuple[i][0])+'.'+str(j))] = 'r'
        elif (temp_tuple[i])[1] == (temp_tuple[i+1])[1]:
            if temp_tuple[i][0] > temp_tuple[i+1][0]:
                temp_list = [temp_tuple[i][0]+1,(temp_tuple[i+1][0])]
            elif temp_tuple[i][0] < temp_tuple[i+1][0]:
                temp_list = [temp_tuple[i][0],(temp_tuple[i+1][0]+1)]
            for j in range(sorted(temp_list)[0],sorted(temp_list)[1]):
                coords[(str(j)+'.'+str(temp_tuple[i][1]))] = 'r'

def sand1():
    s_coord = (500,0)
    global done
    global starti
    global endi
    global startj
    global endj
    while not done:
        if coords[str(s_coord[0])+'.'+str(s_coord[1]+1)] == 'e':
            s_coord = (s_coord[0],s_coord[1]+1)
            if coords[str(s_coord[0])+'.'+str(s_coord[1]-1)] != '+':
                coords[str(s_coord[0])+'.'+str(s_coord[1]-1)] = 'e'

        elif coords[str(s_coord[0]-1)+'.'+str(s_coord[1]+1)] == 'e':
            s_coord = (s_coord[0]-1,s_coord[1]+1)
            if coords[str(s_coord[0]+1)+'.'+str(s_coord[1]-1)] != '+':
                coords[str(s_coord[0]+1)+'.'+str(s_coord[1]-1)] = 'e'

        elif coords[str(s_coord[0]+1)+'.'+str(s_coord[1]+1)] == 'e':
            s_coord = (s_coord[0]+1,s_coord[1]+1)
            if coords[str(s_coord[0]-1)+'.'+str(s_coord[1]-1)] != '+':
                coords[str(s_coord[0]-1)+'.'+str(s_coord[1]-1)] = 'e'

        else:
            done = False
            sand1()

        if s_coord[0] < endi-1 and s_coord[1] < endj-1 and s_coord[1] > startj-1 and s_coord[0] > starti-1:
            coords[str(s_coord[0])+'.'+str(s_coord[1])] = 's'
            
        else:
            done = True

#Part 1

done = False
sand1()

list1=list(coords.values())
print(list1.count('s'))


#Part 2

for i in coords:
    if coords[i] == 's':
        i = 'e'

highest = 0
for i in coords:
    if coords[i] == 'r':
        if int(i.split('.')[1]) > highest:
            highest = int(i.split('.')[1])

for i in range(starti,endi):
    coords[str(i)+'.'+str(highest+2)] = 'r'

def sand2():
    s_coord = (500,0)
    global done
    global starti
    global endi
    global startj
    global endj
    while not done:
        if coords[str(s_coord[0])+'.'+str(s_coord[1]+1)] == 'e':
            s_coord = (s_coord[0],s_coord[1]+1)
            if coords[str(s_coord[0])+'.'+str(s_coord[1]-1)] != '+':
                coords[str(s_coord[0])+'.'+str(s_coord[1]-1)] = 'e'

        elif coords[str(s_coord[0]-1)+'.'+str(s_coord[1]+1)] == 'e':
            s_coord = (s_coord[0]-1,s_coord[1]+1)
            if coords[str(s_coord[0]+1)+'.'+str(s_coord[1]-1)] != '+':
                coords[str(s_coord[0]+1)+'.'+str(s_coord[1]-1)] = 'e'

        elif coords[str(s_coord[0]+1)+'.'+str(s_coord[1]+1)] == 'e':
            s_coord = (s_coord[0]+1,s_coord[1]+1)
            if coords[str(s_coord[0]-1)+'.'+str(s_coord[1]-1)] != '+':
                coords[str(s_coord[0]-1)+'.'+str(s_coord[1]-1)] = 'e'

        else:
            if s_coord != (500,0):
                done = False
                sand2()
            else:
                done = True

        if s_coord[0] < endi-1 and s_coord[1] < endj-1 and s_coord[1] > startj-1 and s_coord[0] > starti-1:
            coords[str(s_coord[0])+'.'+str(s_coord[1])] = 's'
            
        else:
            done = True

done = False
sand2()

list1=list(coords.values())
print(list1.count('s'))

