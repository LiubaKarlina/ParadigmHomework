import numpy as np
import math

def mul_matr(a, b):
    n = len(a)
    if n < 4:
        return a.dot(b)
    n = int(n / 2 )
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

    c11 = t1 + t4 - t5 + t7
    c21 = t2 + t4
    c12 = t3 + t5
    c22 = t1 + t3 - t2 + t6

    return np.vstack((np.hstack((c11,c12)), np.hstack((c21,c22))))

def main():
    n = int(input())
    a = []
    b = []

    for i in range(n):
        a.append(list(map(int, input().split())))
    a = np.array(a)
    for i in range(n):
        b.append(list(map(int, input().split())))
    b = np.array(b)

    if (n & (n - 1)) != 0:
        new_size = 2 ** (int(math.log2(n)) + 1)
        a = np.hstack((a, np.zeros((n,new_size - n))))
        a = np.vstack((a, np.zeros((new_size - n,new_size))))
        b = np.hstack((b, np.zeros((n,new_size - n))))
        b = np.vstack((b, np.zeros((new_size - n,new_size))))

    d = mul_matr(a, b)
    d = d[:n, :n]
    for i in d:
        for x in i:
          print(int(x), end = " ")
        print()

    #for i in d:
    #    print(' '.join(list(map(str, i))))


if __name__ == "__main__":
    main()

