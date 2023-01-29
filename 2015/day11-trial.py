import re

string = "ghjaabcc"

print("iol?", True in [c in string for c in 'iol'])

pairs = re.compile(r'([a-z])\1')
match = pairs.search(string)
if match != None:
  print("Pairs?", match.group(0))
else:
  print("Pairs? False")

"""
sequence = re.compile(r'(?:a(?=b)|b(?=c)|c(?=d)|d(?=e)|e(?=f)|f(?=g)|g(?=h)|h(?=i)|i(?=j)|j(?=k)|k(?=l)|l(?=m)|m(?=n)|n(?=o)|o(?=p)|p(?=q)|q(?=r)|r(?=s)|s(?=t)|t(?=u)|u(?=v)|v(?=w)|w(?=x)|x(?=y)|y(?=z)){2,}')

match = sequence.search(string)
if match != None:
  print("Sequence?", match.group(0))
else:
  print("Sequence? False")
"""

sequence = False
for p in range(len(string)-2):
  if ord(string[p]) == ord(string[p+1]) - 1 and ord(string[p]) == ord(string[p+2]) - 2:
    sequence = True

print("Sequence?", sequence)
