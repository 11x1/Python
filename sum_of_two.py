def sumOfTwo(a, b, v):
    for num in a:
        if v - num in b: return True
    return False

a = [1,6,7,3,2]
b = [3,6,-2,5,6]

print(sumOfTwo(a, b, -1))
