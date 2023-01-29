import json

total = 0

with open("input.json") as f:
  j = json.loads(f.readline())

def handle_list(l):
  sub_total = 0

  for i in l:
    if isinstance(i, int):
      sub_total += i
    elif isinstance(i, list):
      sub_total += handle_list(i)
    elif isinstance(i, dict):
      sub_total += handle_dict(i)

  return sub_total

def handle_dict(d):
  sub_total = 0

  for k in d.keys():
    if isinstance(k, int):
      sub_total += k

    v = d[k]
    if isinstance(v, int):
      sub_total += v
    elif isinstance(v, list):
      sub_total += handle_list(v)
    elif isinstance(v, dict):
      sub_total += handle_dict(v)

  return sub_total

if isinstance(j, int):
  total += j
elif isinstance(j, list):
  total += handle_list(j)
elif isinstance(j, dict):
  total += handle_dict(j)

print("Total:", total)