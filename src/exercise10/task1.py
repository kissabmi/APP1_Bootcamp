try:
    n, need = map(int, input().split())
except:
    print("error")
    exit()

devs = []
for _ in range(n):
    try:
        y, c, t = map(int, input().split())
        devs.append((y, c, t))
    except:
        print("error")
        exit()

if n < 2:
    print("error")
    exit()

years = {}
for y, c, t in devs:
    if y not in years:
        years[y] = []
    years[y].append((c, t))

best = 9999999999
for y, items in years.items():
    items.sort()
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i][1] + items[j][1] == need:
                total = items[i][0] + items[j][0]
                if total < best:
                    best = total

print(best)
