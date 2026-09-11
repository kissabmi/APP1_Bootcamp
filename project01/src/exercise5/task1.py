s = input().strip()

if not s:
    print("error")
    exit()

neg = False
if s[0] == '-':
    neg = True
    s = s[1:]
elif s[0] == '+':
    s = s[1:]

if not s or s == '.':
    print("error")
    exit()

int_part = ""
frac_part = ""
has_dot = False

for ch in s:
    if ch == '.':
        if has_dot:
            print("error")
            exit()
        has_dot = True
    elif ch.isdigit():
        if has_dot:
            frac_part += ch
        else:
            int_part += ch
    else:
        print("error")
        exit()

if int_part == "":
    int_part = "0"
if frac_part == "":
    frac_part = "0"

res = 0
for ch in int_part:
    res = res * 10 + (ord(ch) - 48)

frac_val = 0
for i, ch in enumerate(frac_part):
    frac_val = frac_val * 10 + (ord(ch) - 48)

res += frac_val / (10 ** len(frac_part))

if neg:
    res = -res

res *= 2
print(f"{res:.3f}")
