#Part 2
flag = False
num_list =[]
Alpha_Numbers = {"one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9"}
Reverse_Alpha = {"enin":"9","thgie":"8","neves":"7","xis":"6","evif":"5","ruof":"4","eerht":"3","owt":"2","eno":"1"}
file = open("input1.txt","r")
trace = open("prithm.txt","w")
for line in file:
    line=line.strip()
    #print(line)
    temp = []
    temp2=[]
    reverse =(line[::-1])
    #print(reverse)
    for x,number in enumerate(Alpha_Numbers):
        if line.find(number) >-1:
            #print(line.index(number),number)
            temp2.append([line.index(number),Alpha_Numbers[number]])
            #line = line.replace(number,"")
    #print(temp2)
   
    for item in Reverse_Alpha:
        if reverse.find(item)>-1:
            #print(len(line)-1-reverse.find(item),Reverse_Alpha[item])
            temp2.append([len(line)-1-reverse.find(item),Reverse_Alpha[item]])
    #print("here",temp2)
   
    for x,character in enumerate(line):
        if character.isnumeric():
            #print("one",x,character)
            temp2.append([x,character])
    #print(temp2)
    temp2.sort()
    #print(temp2)

            #print(x,len(line)-1)

    print(temp2[0][1]+temp2[-1][1], line, reverse, temp2, file=trace)
    num_list.append([temp2[0][1]+temp2[-1][1]])
           
#print(num_list)
total = 0
for item in num_list:
    #print(item)
    total += int(item[0])
print(total)
trace.close()