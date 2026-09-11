try:
    n = int(input())
except:
    print("Natural number was expected")
    exit()

if n <= 0:
    print("Natural number was expected")
    exit()

row = [1]
for i in range(n):
    print(" ".join(map(str, row)))
    nxt = [1]
    for j in range(len(row) - 1):
        nxt.append(row[j] + row[j + 1])
    nxt.append(1)
    row = nxt
