import resource
import sys, resource

from tqdm import tqdm

from _lambdas import EMPTY, HEAD, TAIL, TRUE


sys.setrecursionlimit(1000000)
resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))


_inc = lambda x: x + 1
decode_natural = lambda x: x(_inc)(0)


def decode_list(encoded):
    decoded = []
    for _ in range(10000000000):
        if EMPTY(encoded) is TRUE:
            return decoded
        decoded.append(HEAD(encoded))
        encoded = TAIL(encoded)
    raise RuntimeError('probably infinite list')


def get_pbar(n):
    total = lambda n: len(list((x, y) for x in range(1, n) for y in range(1, x+1)))
    pbar = tqdm(total=total(n), position=0, leave=True)
    def inc_pbar(x):
        pbar.update(1)
        return x
    return pbar, inc_pbar
