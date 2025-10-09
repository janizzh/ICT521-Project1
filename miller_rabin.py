import random
import time  # For measuring testing time

die = random.SystemRandom()  # A secure random number generator

def single_test(n, a):
    """
    Take number n and test it for primeness using witness a.
    Returns True if n passes this round of Miller-Rabin, False otherwise.
    """
    exp = n - 1
    while not exp & 1:  # While exp is even
        exp >>= 1  # Bit manipulation equivalent to exp // 2

    if pow(a, exp, n) == 1:
        return True

    while exp < n - 1:
        if pow(a, exp, n) == n - 1:
            return True
        exp <<= 1

    return False  # If none of the terms above succeed, n is composite

def miller_rabin(n, k=40):
    """
    Probabilistic Miller-Rabin primality test.
    k = number of random witnesses to test.
    Returns True if n is probably prime, False if composite.
    """
    #  Handle small inputs to avoid randrange(2, 2) errors
    if n < 4:
        return n == 2 or n == 3

    for i in range(k):
        a = die.randrange(2, n - 1)  # Random witness 1 < a < n - 1
        if not single_test(n, a):
            return False  # Composite
    return True  # Probably prime

def gen_prime(bits):
    """
    Generate a prime number with the specified number of bits.
    Generates large odd numbers and tests them using Miller-Rabin.
    """
    while True:
        a = (die.randrange(1 << (bits - 1), 1 << bits) << 1) + 1  # Ensure odd number
        if miller_rabin(a):
            return a

# Generate two 1024-bit prime numbers
if __name__ == "__main__": # Prevent this part of code from running, when importing the file
    print("Generating first 1024-bit prime...")
    p_one = gen_prime(1024)
    print("Generating second 1024-bit prime...")
    p_two = gen_prime(1024)

# -------------------------------
# Measure testing time for p_one
    start_time = time.time()
    result_one = miller_rabin(p_one)
    end_time = time.time()
    print("\np_one:", p_one)
    print("p_one is prime:", result_one)
    print("Time to test p_one:", end_time - start_time, "seconds")

# Measure testing time for p_two
    start_time = time.time()
    result_two = miller_rabin(p_two)
    end_time = time.time()
    print("\np_two:", p_two)
    print("p_two is prime:", result_two)
    print("Time to test p_two:", end_time - start_time, "seconds")

# -------------------------------
# Alternatively: Multiply the two primes to show the product is composite
# print("\nMultiplication of p_one and p_two (will be composite):")
# print(p_one * p_two)
# Note: The multiplication result can be checked using a third-party tool if desired
