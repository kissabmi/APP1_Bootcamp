n = int(input())

if n < 0:
    print(False)
else:
    original = n
    reversed_num = 0
    while n > 0:
        reversed_num = reversed_num * 10 + n % 10
        n //= 10
    print(original == reversed_num)
