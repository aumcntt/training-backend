import math

#Bài 1
def is_primary(x):
    if x <= 1:
        return False
    elif x == 2:
        return True
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True

def sum_primary(n):
    if n < 2 :
        return 0
    if n == 2 :
        return 2
    sum_result = 0
    for i in range(2, n+1):
        if is_primary(i):
            sum_result += i

    return sum_result

bt1 = int(input("Nhập số nguyên dương n: "))
print(f"Tổng các số nguyen tố từ 1 đến n {sum_primary(bt1)}")

#Bài 2
def is_palindrome(x):
    if x < 0:
        return False
    if x < 10:
        return True
    x_str = str(x)
    for i in range(len(x_str) // 2):
        if x_str[i] != x_str[len(x_str) - 1 - i]:
            return False
    return True

bt2 = int(input("Nhập số nguyên dương n: "))
print(f'{"Đây là số palindrome" if is_palindrome(bt2) else "Đây không phải số palindrome"}')


#Bài 3
def is_square(n):
    return math.sqrt(n) == int(math.sqrt(n))

#Cách 1 sử dụng filter
def list_square_1(n):
    if n < 1:
        return []

    a = [x for x in range(1, n + 1)]

    result = filter(is_square, a)

    return list(result)

#Cách 2 sử dụng map
def list_square_2(n):
    if n < 1:
        return []

    a = [x for x in range(1, n + 1)]

    result = map(lambda x: x if is_square(x) else None, a)
    result = [x for x in result if x is not None]

    return list(result)

bt3 = int(input("Nhập số nguyên dương n: "))
print(f"Danh sách các số chính phương tu 1 tới n dùng filter {list_square_1(bt3)}")
print(f"Danh sách các số chính phương tu 1 tới n dùng map {list_square_2(bt3)}")


