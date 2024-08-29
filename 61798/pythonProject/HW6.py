""" Q1 """


def schoolbook_method(a: str, b: str) -> str:
    """
    :param a: 1st multiply number
    :param b: 2nd multiply number
    :return: the multiply result string
    """
    str_a = a if isinstance(a, str) else str(a)
    str_b = b if isinstance(b, str) else str(b)

    res = [0] * (len(str_a) + len(str_b))

    for i in range(len(str_b) - 1, -1, -1):
        # carry bit
        c = 0
        for j in range(len(str_a) - 1, -1, -1):
            # current product
            p = (int(str_b[i]) * int(str_a[j])) + c + res[i + j + 1]
            c = p // 10
            res[i + j + 1] = p % 10
        res[i] += c

    str_res = ''.join(map(str, res)).lstrip('0')
    if not str_res:
        return '0'
    return str_res


def horners_method(coefs: list, x) -> float:
    """
    :param a: list of polynomial coefs, from the highest degree term to constant term
    :param x: the eval point
    :return: the value of the evaluation
    """
    res = coefs[0]
    for i in range(1, len(coefs)):
        res = res * x + coefs[i]
    return res


a, b = input("Q1: input the factors a and b: ").split()
print(f"Result of schoolbook method: {schoolbook_method(a, b)}")

coefs = [float(e) for e in input("Q1: input the coefficients of polynomial: ").split()]
x = float(input("Q1: input the point x: "))
print(f"Result of Horner\'s method: {horners_method(coefs, x)}")


""" Q2 """

# give the p_4(n) = 1^4 + 2^4 + ... + n^4
# and the summation of this series is: sum(p_4(n)) = n * (n+1) * (2n+1) * (3n^2+3n-1) / 30
# in the limit of n, the growth of the series is mainly determined by the highest degree term,
# which can be found to be 5 by the summation formula,
# so the progressive growth of p4(n) is O(n^5).
# it could be proved via plot:

import numpy as np
import matplotlib.pyplot as plt


def p4(n: int) -> int:
    return n * (n + 1) * (2 * n + 1) * (3 * n ** 2 + 3 * n - 1) // 30


n = np.arange(1, 50)
p4_series = np.array([p4(e) for e in n])
n5_series = n ** 5

plt.plot(n, p4_series, label='$p_4(n) = 1^4 + 2^4 + ... + n^4$')
plt.plot(n, n5_series, label='$n^5$', linestyle='--')
plt.xlabel('n')
plt.ylabel('Value')
plt.yscale('log')  # using log scaled axis 'cause it would be overflowed

plt.legend()
plt.show()

""" Q3 """
# the temperature mixing is assumed to be weighted in the ideal regime
# the first time, because we can only pour 25%, so need a weighted average,
# and then we can pour 50% each time, which can be regarded as an average
# Since the capacity of the final two cups of water is not enforced in the problem,
# we do not consider the final average water capacity
v1, v2 = 0.75, 0.75
t1, t2 = 50, 100
temp_diff = t2 - t1
step = 0
while temp_diff > 1:
    if step == 0:
        t1_new = (v1 * t1 + (1 - v2) * t2)
        t2_new = t2
    else:
        if step % 2 == 1:
            t1_new = (t1 + t2) / 2
            t2_new = t2
            v1, v2 = 0.5, 1
        else:
            t2_new = (t1 + t2) / 2
            t1_new = t1
            v1, v2 = 1, 0.5
    t1, t2 = t1_new, t2_new
    temp_diff = abs(t2 - t1)
    # print(f"{t1}, {t2}, {temp_diff}")
    step += 1

print(f"Q3: The step they need is: {step}")

import math

""" Q4 """


def f(x):
    return x - 2 * math.sin(x)


def bisection(a, b, epsilon=1e-4, max_iter=100):
    n = 0
    while (b - a) / 2 > epsilon and n < max_iter:
        midpoint = (a + b) / 2
        if f(midpoint) == 0:
            break
        elif f(a) * f(midpoint) < 0:
            b = midpoint
        else:
            a = midpoint
        n += 1
    return (a + b) / 2, n


x, n = bisection(a=0, b=np.pi, epsilon=1e-4, max_iter=100)
print(f"Q4: number of iterations with eps=1e-4: {n}, root is {x}")
print("The final result is very close to the positive solution, so the bisection method is valid")

""" Q5 """
# the exact calculation of the square root of 2 can be done using Newton-laverson iteration method
# the iteration formula is: x_(n+1) = x_n - f(x_n) / f'(x_n), and proof step is:
# 1. The Taylor series expansion of f of x at xn is: f(x) = f(x_n) + (x-x_n)f'(x_n) + R_n(x_n^2)
#       R_n(x_n^2) is the Lagrangian remainder
# 2. The Lagrangian remainder can be ignored, so a linear approximation can be obtained:
#       f(x) = f(x_n) + (x-x_n)f'(x_n)
# 3. Let f(x) = 0, and then we could get the root x = x_n - f(x_n) / f'(x_n)

from decimal import Decimal

x = Decimal(1)
for _ in range(1000):
    x = (x + Decimal(2) / x) / 2
print(f"Q5: the final approximation root of sqrt(2) is: {str(x)[0:1002]}")
print("python can't show that many bits because of the bit limit, but the calculation is efficient")


""" Q6 """


def longest_substring(str1: str, str2: str):
    m, n = len(str1), len(str2)
    min_length = min(m, n)
    max_common_length = 0

    for length in range(1, min_length + 1):
        substrings = set()
        for i in range(m - length + 1):
            substrings.add(str1[i:i + length])

        for i in range(n - length + 1):
            if str2[i:i + length] in substrings:
                max_common_length = length

    if max_common_length > 0:
        return str1[:max_common_length]
    return ""


s1, s2 = input("Q6: please input 2 strings separated: ").split()
substring = longest_substring(s1, s2)
print(f"the longest substring is {substring}, its length is {len(substring)}")
