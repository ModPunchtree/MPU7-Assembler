

immedateValues = [1, 3, 31, 63, 56, 56, 127, 255, 255, 63, 63, 63, 248, 248, 127, 63, 63, 120, 248, 249, 57, 57, 57, 249, 249, 120, 60, 63, 63, 31, 3, 1, 140, 142, 255, 255, 3, 1, 249, 249, 249, 249, 249, 249, 1, 3, 255, 255, 255, 1, 1, 255, 159, 143, 135, 131, 145, 25, 61, 255, 255, 255, 142, 140, 49, 113, 255, 255, 192, 128, 159, 159, 159, 159, 159, 159, 143, 207, 255, 255, 255, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 113, 49, 128, 192, 248, 252, 60, 28, 158, 159, 159, 156, 156, 156, 31, 63, 254, 252, 252, 30, 31, 159, 156, 156, 156, 159, 159, 158, 156, 252, 252, 248, 192, 128]

uniqueValues = [[420, 69]]

for imm in immedateValues:
    nums = [i[0] for i in uniqueValues]
    if imm not in nums:
        uniqueValues.append([imm, 1])
    else:
        uniqueValues[nums.index(imm)][1] += 1

uniqueValues.pop(0)

def foo(x):
    return x[1]

uniqueValues.sort(reverse = True, key = foo)

print(uniqueValues)

