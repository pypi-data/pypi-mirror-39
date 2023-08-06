# loglikelihood:

from sympy import *

t, u, s, d = symbols("t u s d")


def pdf(x):
    return 1 / sqrt(2 * pi) * exp(-x ** 2 / 2)


def cdf(x):
    return (1 + erf(x / sqrt(2))) / 2


ds = diff(d * log(pdf((log(t) - u) / s) / (t * s * (1 - cdf((log(t) - u) / s)))) + log(1 - cdf((log(t) - u) / s)), s)
