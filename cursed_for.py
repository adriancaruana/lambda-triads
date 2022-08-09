import sys

from _lambdas import LTE, GTE, ADD, NOT, TRUE, Y, FALSE
from _lambdas import ZERO, ONE, TWO, THREE, TEN, LIST, APPEND
from _helpers import *


# We want to do something like this:

"""
FOR(i := ZERO)(LEQ(i)(TEN))(ADD(i)(ONE))(
    print(i)
)
"""

# Let's get started

# If we want to use LTE, we need to make the loop 
# var the last of the curried arguments. This is a little 
# bit backwards, so we will call it RLTE (for Reverse) 
# for clarity.
RLEQ = lambda x: lambda y: LTE(y)(x)
# This is essentially GTE, so we could just use that instead.

# Now, we need to define FOR. FOR is a function with 
# four arguments, VAR, COND, INC, and BODY.
FOR = Y(
    lambda f: lambda VAR: lambda COND: lambda INC: lambda BODY: (
        NOT(COND(VAR))  # This is the break clause
        (lambda _: VAR)  # If the break clause is TRUE, return VAR
        # This is where the for-loop executes. We need to do 3 things:
        # - Execute the body of the loop: BODY(...)
        # - Increment VAR: INC(...)
        # - Proceed to the next iteration: f(next i)(COND)(INC)(BODY)
        # Note that the first argument to the Y-Combinator is the function 
        # itself. I.e., f == FOR
        (lambda _: f(INC(BODY(VAR)))(COND)(INC)(BODY))
        (FALSE)
    )
)

LI = LIST

# Now, lambda is stateless (i.e., it can have no side effects).
# Whereas, the C for loop is inherently stateful
# So if we want to see what happens at different iterations 
# within the loop, BODY needs to be stateful
def BODY(x):
    global LI
    LI = APPEND(LI)(x)
    print(list(map(decode_natural, decode_list(LI))))
    return x


# We can now run it like this:
r = FOR(ZERO)(RLEQ(TEN))(ADD(ONE))(
    BODY
)