import re

password = "abcdefgh"
password = "ghijklmn"
password = "vzbxkghb" # part 1 input
password = "vzbxxyzz" # part 2 input

#sequence = re.compile(r'(?:a(?=b)|b(?=c)|c(?=d)|d(?=e)|e(?=f)|f(?=g)|g(?=h)|h(?=i)|i(?=j)|j(?=k)|k(?=l)|l(?=m)|m(?=n)|n(?=o)|o(?=p)|p(?=q)|q(?=r)|r(?=s)|s(?=t)|t(?=u)|u(?=v)|v(?=w)|w(?=x)|x(?=y)|y(?=z)){3,}')
pairs = re.compile(r'([a-z])\1.*([a-z])\2')

def is_legal(potential):
  if True in [c in potential for c in 'iol']:
    #print(potential,"contains iol")
    return False

  #smatches = sequence.search(potential)
  #if smatches == None:
    #print(potential,"contains no sequence")
    #return False

  sequence = False
  for p in range(len(potential)-2):
    if ord(potential[p]) == ord(potential[p+1]) - 1 and ord(potential[p]) == ord(potential[p+2]) - 2:
      sequence = True
  if not sequence:
    #print(potential,"contains no sequence")
    return False

  pmatches = pairs.search(potential)
  if pmatches == None:
    #print(potential,"contains no pairs")
    return False

  return True

def inc_password(value):
  value = value[::-1]
  
  keep_going = True
  column = 0
  while keep_going:
    value = value[0:column] + chr(((ord(value[column]) - 97 + 1) % 26) + 97) + value[column+1:]
    if value[column] != 'a':
      keep_going = False
    else:
      column += 1

  return value[::-1]

password = inc_password(password)
while not is_legal(password):
  #print(password,"-> illegal")
  password = inc_password(password)

print(password)