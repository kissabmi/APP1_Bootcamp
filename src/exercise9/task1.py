n, x = input().split()
n = int(n)
x = float(x)

c = [float(input()) for _ in range(n + 1)]

d = 0

for i in range(n):
    p = n - i
    d += c[i] * p * (x ** (p - 1))

print(f"{d:.3f}")
