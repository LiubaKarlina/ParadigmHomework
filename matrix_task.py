import numpy as np
import math

def mul_matr(a, b):
    n = len(a)
    result = np.empty((n,n), dtype = int)
    if n < 4:
        return a.dot(b)
    n = n // 2
    a11 = a[:n,:n]
    a12 = a[:n, n:]
    a21 = a[ n:, :n]
    a22 = a[ n:,n:]

    b11 = b[:n, :n]
    b12 = b[:n, n:]
    b21 = b[n:, :n]
    b22 = b[n:, n:]

    t1 = mul_matr(a11 + a22, b11 + b22)
    t2 = mul_matr(a21 + a22, b11)
    t3 = mul_matr(a11, b12 - b22)
    t4 = mul_matr(a22, b21 - b11)
    t5 = mul_matr(a11 + a12, b22)
    t6 = mul_matr(a21 - a11, b11 + b12)
    t7 = mul_matr(a12 - a22, b21 + b22)

    result[:n, :n] = t1 + t4 - t5 + t7
    result[:n, n:2 * n] = t3 + t5
    result[n:n * 2, :n] = t2 + t4
    result[n:2 * n, n:2 * n] = t1 + t3 - t2 + t6
    return result

def get_matrix(n):
    a = np.empty((n,n))

    for i in range(n):
        a[i] = list(map(int, input().split()))

    return a

def get_resize_matrix(n):
    new_size = n
    if (n & (n - 1)) != 0:
        new_size = 2 ** (n.bit_length())
    matrix = np.zeros((new_size, new_size), dtype=int)
    matrix[:n, :n] = get_matrix(n)
    return matrix

def main():
    n = int(input())

    matrix1 = get_resize_matrix(n)
    matrix2 = get_resize_matrix(n)

    d = mul_matr(matrix1, matrix2)
    d = d[:n, :n]
    print(matrix1.dot(matrix2))

    for i in d:
        print(' '.join(list(map(str, i))))


if __name__ == "__main__":
    main()