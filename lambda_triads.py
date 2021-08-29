#!/usr/bin/python3
# Pythagorean Triads, using Lambda Calculus, implemented in Python
# Author: Adrian Caruana
# Run it like this: ./lambda_triads.py "MULT(TEN)(ONE)"
import sys

from _lambdas import *
from _helpers import *


N = eval(sys.argv[1])
n = decode_natural(N)
pbar, inc_pbar = get_pbar(n)


CONCAT = Y(
    lambda f: lambda l0: lambda l1: EMPTY(l0)
    (lambda _: l1)
    (lambda _: PREPEND(f(DROP(ONE)(l0))(l1))(HEAD(l0)))
    (TRUE)
)

CANDIDATES = Y(
    lambda f: lambda i: lambda j: lambda stop: OR(GT(i)(stop))(GT(j)(i))
    # inner f(i)(INC(j))(i)
    # outer f(INC(i))(j)(stop)
    (lambda _: LIST)
    (lambda _: PREPEND(CONCAT(f(i)(INC(j))(i))(f(INC(i))(j)(stop)))(PAIR(i)(j))
    )
    (TRUE)
)

LI_ZERO_TO_N = Y(
    lambda f: lambda n: EQ(n)(ZERO)
    (lambda _: LIST)
    (lambda _: PREPEND(f(DEC(n)))(n))
    (FALSE)
)

Z_LUT = (
    lambda n: 
    MAP
    (lambda x: PAIR(x)(EXP(x)(TWO)))
    (LI_ZERO_TO_N(n))
)

INT_SQRT = Y(
    lambda f: lambda a2b2: lambda z: OR(EMPTY(z))(GT(a2b2)(SECOND(HEAD(z))))
    (lambda _: ZERO)
    (lambda _: EQ(SECOND(HEAD(z)))(a2b2)(FIRST(HEAD(z)))(f(a2b2)(DROP(ONE)(z))))
    (TRUE)
)

A2B2 = lambda x: ADD(EXP(FIRST(x))(TWO))(EXP(SECOND(x))(TWO))

GET_TRIADS = (
    lambda candidates:
    MAP
    (lambda x: inc_pbar(PAIR(x)(INT_SQRT(A2B2(x))(Z_LUT(N)))))
    (candidates)
)
TRIAD_LI = lambda triads: FILTER(lambda x: NOT(ISZERO(SECOND(x))))(triads)


if __name__ == "__main__":
    # From a list of pairs, (a, b), determine
    # which pairs (a, b) have integer hypotenuse c.
    # Returns a list of triads ((a, b), c).
    TRIADS = TRIAD_LI(GET_TRIADS(CANDIDATES(ONE)(ONE)(N)))

    pbar.close()
    # Decode and print
    triads = []
    for I in decode_list(RANGE(ZERO)(LENGTH(TRIADS))):
        x = INDEX(I)(TRIADS)
        triads.append(
            (
                decode_natural(FIRST(FIRST(x))), 
                decode_natural(SECOND(FIRST(x))), 
                decode_natural(SECOND(x)),
            )
        )
    print(triads)
