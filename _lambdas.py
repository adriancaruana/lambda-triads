# Lambdas
# Derived from:
# https://github.com/orsinium-labs/python-lambda-calculus

# bool
ID = lambda x: x
TRUE = lambda x: lambda y: x
FALSE = lambda x: lambda y: y

# Logic
NOT = lambda x: x(FALSE)(TRUE)
AND = lambda x: lambda y: x(y)(x)
OR  = lambda x: lambda y: x(x)(y)
XOR = lambda x: lambda y: x(NOT(y))(y)
XNOR = lambda x: lambda y: NOT(XOR(x)(y))

# Church Numerals
# 0 := λf.λx.x
# 1 := λf.λx.f x
# 2 := λf.λx.f (f x)
# 3 := λf.λx.f (f (f x))
ZERO   = lambda f: lambda x: x
ONE    = lambda f: lambda x: f(x)
TWO    = lambda f: lambda x: f(f(x))
THREE  = lambda f: lambda x: f(f(f(x)))
FOUR   = lambda f: lambda x: f(f(f(f(x))))
FIVE   = lambda f: lambda x: f(f(f(f(f(x)))))
SIX    = lambda f: lambda x: f(f(f(f(f(f(x))))))
SEVEN  = lambda f: lambda x: f(f(f(f(f(f(f(x)))))))
EIGHT  = lambda f: lambda x: f(f(f(f(f(f(f(f(x))))))))
NINE   = lambda f: lambda x: f(f(f(f(f(f(f(f(f(x)))))))))
TEN    = lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))

# Arithmetic
INC = lambda n: lambda f: lambda x: f(n(f)(x))
ADD = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))
MULT = lambda m: lambda n: lambda f: lambda x: m(n(f))(x)
EXP = lambda m: lambda n: n(m)
DEC = lambda n: lambda f: lambda x: n(lambda g: lambda h: h(g(f)))(lambda _: x)(ID)
SUB = lambda m: lambda n: n(DEC)(m)
DIFF = lambda m: lambda n: ADD(SUB(m)(n))(SUB(n)(m))

# Compare
ISZERO = lambda x: x(lambda _: FALSE)(TRUE)
GTE    = lambda x: lambda y: ISZERO(SUB(y)(x))
LTE    = lambda x: lambda y: ISZERO(SUB(x)(y))
GT     = lambda x: lambda y: ISZERO(SUB(INC(y))(x))
LT     = lambda x: lambda y: ISZERO(SUB(INC(x))(y))
EQ     = lambda x: lambda y: AND(GTE(x)(y))(LTE(x)(y))
MIN    = lambda x: lambda y: LTE(x)(y)(x)(y)
MAX    = lambda x: lambda y: GTE(x)(y)(x)(y)

# Pairs
PAIR = lambda x: lambda y: lambda z: z(x)(y)
FIRST = lambda p: p(TRUE)
SECOND = lambda p: p(FALSE)

# Y-Combinator
Y = lambda f: (
    (lambda x: f(lambda y: x(x)(y)))
    (lambda x: f(lambda y: x(x)(y)))
)

# Lists
LIST = PAIR(TRUE)(TRUE)
PREPEND = lambda xs: lambda x: PAIR(FALSE)(PAIR(x)(xs))
EMPTY = lambda xs: FIRST(xs)
HEAD = lambda z: FIRST(SECOND(z))
TAIL = lambda z: SECOND(SECOND(z))

# List Ops
APPEND = Y(
    lambda f: lambda xs: lambda x: EMPTY(xs)
    (lambda _: PREPEND(xs)(x))
    (lambda _: PAIR(FALSE)(PAIR(HEAD(xs))(f(TAIL(xs))(x))))
    (TRUE)
)
REVERSE = Y(
    lambda f: lambda xs: EMPTY(xs)
    (lambda _: LIST)
    (lambda _: APPEND(f(TAIL(xs)))(HEAD(xs)))
    (TRUE)
)
# MAP(a)(xs): apply `a` function to every element in `xs` list.
# Return list of results for every element.
MAP = Y(
    lambda f: lambda a: lambda xs: EMPTY(xs)
    (lambda _: LIST)
    (lambda _: PREPEND(f(a)(TAIL(xs)))(a(HEAD(xs))))
    (TRUE)
)
RANGE = Y(
    lambda f: lambda a: lambda b: GTE(a)(b)
    (lambda _: LIST)
    (lambda _: PREPEND(f(INC(a))(b))(a))
    (TRUE)
)
# REDUCE(r)(l)(v):
# 1. Apply pass head of `l` and `v` into `r` and save result into `v`.
# 2. Do it for every element into lest from left to right.
# 3. Return `v` (accumulated value)
REDUCE = FOLD = Y(
    lambda f: lambda r: lambda l: lambda v: EMPTY(l)
    (lambda _: v)  # if list is empty, return accumulated value (v)
    # pass accumulated value (v) and head into reducer (r)
    # do reucing on tail of list (l) with a new accumulated value (v)
    (lambda _: f(r)(TAIL(l))(r(HEAD(l))(v)))
    (TRUE)
)
FILTER = lambda f: lambda l: (
    REDUCE
    (lambda x: lambda xs: f(x)(APPEND(xs)(x))(xs))
    (l)
    (LIST)
)
DROP = lambda n: lambda l: n(TAIL)(l)
TAKE = Y(lambda f: lambda n: lambda l: (
    OR(EMPTY(l))(ISZERO(n))
    (lambda _: LIST)
    (lambda _: (
        PREPEND(f(DEC(n))(TAIL(l)))
        (HEAD(l))
    ))
    (TRUE)
))
LENGTH = lambda l: REDUCE(lambda x: lambda n: INC(n))(l)(ZERO)
INDEX = Y(lambda f: lambda n: lambda l: (
    ISZERO(n)
    (lambda _: HEAD(l))
    (lambda _: f(DEC(n))(TAIL(l)))
    (TRUE)
))
ANY = Y(lambda f: lambda l: (
    EMPTY(l)
    (lambda _: FALSE)
    (lambda _: HEAD(l)(TRUE)(f(TAIL(l))))
    (TRUE)
))
ALL = Y(lambda f: lambda l: (
    EMPTY(l)
    (lambda _: TRUE)
    (lambda _: NOT(HEAD(l))(FALSE)(f(TAIL(l))))
    (TRUE)
))
