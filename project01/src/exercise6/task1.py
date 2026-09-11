import json

with open("input.txt") as f:
    c = f.read().strip()

if not c:
    print("Empty file")
    exit()

try:
    d = json.loads(c)
except:
    print("error")
    exit()

l1 = d.get("list1", [])
l2 = d.get("list2", [])

if not isinstance(l1, list) or not isinstance(l2, list):
    print("error")
    exit()

for m in l1:
    if not isinstance(m, dict) or "title" not in m or "year" not in m:
        print("error")
        exit()

for m in l2:
    if not isinstance(m, dict) or "title" not in m or "year" not in m:
        print("error")
        exit()

res = []
i = j = 0
while i < len(l1) and j < len(l2):
    if l1[i]["year"] <= l2[j]["year"]:
        res.append(l1[i])
        i += 1
    else:
        res.append(l2[j])
        j += 1

while i < len(l1):
    res.append(l1[i])
    i += 1

while j < len(l2):
    res.append(l2[j])
    j += 1

print(json.dumps({"list0": res}, indent=2, ensure_ascii=False))
