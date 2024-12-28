def ternary(num):
    string = ''
    while num != 0:
        string = str(num % 3) + string
        num //= 3
    
    return string

print(ternary(1))
print(ternary(2))
print(ternary(3))
print(ternary(4))
print(ternary(5))
print(ternary(6))