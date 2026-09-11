from typing import List
from math import sqrt, floor
# a)
def nearest_armstrong(n: int) -> int:
    # walk out from n
    # on first encountered armstrong number, return
    dst = 0
    while True:
        if is_armstrong(n + dst): return n + dst
        if is_armstrong(n - dst): return n - dst
        dst += 1


def is_armstrong(n: int) -> bool:
    if n < 0: return False
    
    digits = [int(c) for c in str(n)]
    digits_ct = len(digits)
    raised_digits = [d ** digits_ct for d in digits]
    raise_digits_sum = sum(raised_digits)
    
    return  raise_digits_sum == n

# b)
def primes(a: int, b: int) -> List[int]:
    prime_list = [n for n in range(a, b + 1) if is_prime(n)]
    
    return prime_list

def is_prime(n: int) -> bool:
    for candidate in range(2, floor(sqrt(n)) + 1):
        if n % candidate == 0:
            return False
        
    return True

