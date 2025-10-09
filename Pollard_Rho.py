# Import the Miller-Rabin primality test code from miller_rabin.py file
from miller_rabin import miller_rabin

import random
import math
import time

# A secure random number generator
die = random.SystemRandom()

# Finds a non-trivial factor of n
def pollard_rho(n):
    # Handle trivial cases
    if n % 2 == 0:  # Even numbers are always divisible by 2
        return 2
    if n == 1:
        return 1

    # Repeat until a factor is found
    while True:
        # Random starting values for the algorithm
        x = die.randrange(2, n - 1)
        y = x
        c = die.randrange(1, n - 1)  #
        d = 1                        # GCD value

        # Floyd’s cycle-finding algorithm
        while d == 1:
            # Generate next x and y using the function f(x) = (x^2 + c) mod n
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n  # y moves twice as fast as x

            # Compute the GCD of |x - y| and n
            d = math.gcd(abs(x - y), n)

            # If d == n, the attempt failed, restart with new parameters
            if d == n:
                break

        # If a non-trivial factor (1 < d < n) is found, return it
        if 1 < d < n:
            return d



# Function to fully factorize an integer using Pollard Rho
def factorize(n):
    # Base case: 1 has no factors
    if n == 1:
        return []

    # Handle even numbers directly
    if n % 2 == 0:
        return [2] + factorize(n // 2)

    # If n is prime, return it as a factor
    if miller_rabin(n):  # Imported from miller_Rabin.py file
        return [n]

    # Otherwise, try finding a non-trivial factor using Pollard Rho
    d = pollard_rho(n)

    # If Pollard Rho fails and returns n, treat n as prime
    if d == n:
        return [n]

    # Factorize both parts: d and n/d
    return factorize(d) + factorize(n // d)



# Factorize (p - 1)/2 for two large primes
if __name__ == "__main__":
    # Replace with any prime number
    p_one = 10007

    p_two = 65537

    # Loop through both primes and factorize (p - 1)/2 for each
    for name, p in [("p_one", p_one), ("p_two", p_two)]:
        print(f"\n{'='*60}")
        print(f"Factoring ({name} - 1) / 2 ...")

        # Compute (p - 1) / 2
        n = (p - 1) // 2

        # Measure how long the factorization takes
        start = time.time()
        factors = factorize(n)
        end = time.time()

        # Print results
        print(f"\n({name} - 1)/2 = {n}")
        print("Factors found:", factors)
        print("Time taken:", round(end - start, 4), "seconds")

        # Determine whether non-trivial factors were found
        if len(factors) == 1:
            print("No non-trivial factors found (number is likely prime).")
        else:
            print("Non-trivial factors found.")
