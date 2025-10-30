# ======================================================
# Pollard Rho (Floyd variant) with safeguards
# ======================================================

import math
import random
import time
from miller_rabin import miller_rabin  # Keep your Miller-Rabin
try:
    from generated_primes import p_one, p_two
except ImportError:
    raise FileNotFoundError("generated_primes.py not found. Run miller_rabin.py first.")

# Secure random number generator
die = random.SystemRandom()

# ------------------------------------------------------
# Floyd's Pollard Rho algorithm with max iteration limit
# ------------------------------------------------------
def pollard_rho_floyd(n, max_iter=1_000_000):
    """
    Attempts to find a non-trivial factor of n using Floyd's Pollard Rho.
    Returns a factor if found, None otherwise.
    max_iter: maximum number of iterations before giving up.
    """
    if n % 2 == 0:
        return 2
    if n == 1:
        return 1

    iter_count = 0
    while True:
        x = die.randrange(2, n - 1)
        y = x
        c = die.randrange(1, n - 1)
        d = 1

        while d == 1:
            # Increment iteration counter
            iter_count += 1
            if iter_count > max_iter:
                return None  # Give up after too many iterations

            # Floyd's iteration
            x = (x*x + c) % n
            y = (y*y + c) % n
            y = (y*y + c) % n
            d = math.gcd(abs(x - y), n)

            if d == n:  # Failed attempt, restart
                break

        if 1 < d < n:
            return d

# ------------------------------------------------------
# Factorization wrapper with retries and primality check
# ------------------------------------------------------
def factor_number(n, max_retries=5, max_iter=1_000_000):
    """
    Attempts to find a non-trivial factor of n using Floyd's Pollard Rho.
    Returns (factor or None, elapsed time).
    """
    start_time = time.perf_counter()

    # Step 1: Skip if prime
    if miller_rabin(n):
        return None, 0.0

    # Step 2: Try multiple random seeds
    for _ in range(max_retries):
        factor_candidate = pollard_rho_floyd(n, max_iter=max_iter)
        if factor_candidate and factor_candidate != n:
            return factor_candidate, time.perf_counter() - start_time

    # Step 3: Give up if no factor found
    return None, time.perf_counter() - start_time

# ------------------------------------------------------
# MAIN
# ------------------------------------------------------
if __name__ == "__main__":
    for name, p in [("p_one", p_one), ("p_two", p_two)]:
        print(f"\n{'='*70}")
        print(f"Factoring ({name}-1)//2 ...")

        n = (p-1)//2
        print(f"Bit length of (p-1)//2: {n.bit_length()}")

        # Step 1: Check primality
        if miller_rabin(n):
            print(f"(p-1)//2 is probably prime → no non-trivial factors")
            continue

        # Step 2: Factor
        factor, elapsed = factor_number(n, max_retries=5, max_iter=1_000_000)
        if factor:
            print(f"Found factor: {factor}")
            print(f"Time taken: {elapsed:.6f} seconds")
        else:
            print("No factor found → likely prime or very hard to factor")
            print(f"Elapsed time: {elapsed:.6f} seconds")
