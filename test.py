
sum = 0
for i in range(1 , 8):
    a = pow(3 , i)
    sum = a + sum
    print(f"{a} - {i} star")
print(f"Total sum is {sum}")