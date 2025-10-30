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
        exp >>= 1  # Divide by 2 until odd

    if pow(a, exp, n) == 1:
        return True

    while exp < n - 1:
        if pow(a, exp, n) == n - 1:
            return True
        exp <<= 1

    return False  # Composite


def miller_rabin(n, k=40):
    """
    Probabilistic Miller-Rabin primality test.
    k = number of random witnesses to test.
    Returns True if n is probably prime, False if composite.
    """
    if n < 4:
        return n == 2 or n == 3

    for _ in range(k):
        a = die.randrange(2, n - 1)
        if not single_test(n, a):
            return False
    return True


def gen_prime(bits):
    """
    Generate a prime number with the specified number of bits.
    Generates large odd numbers and tests them using Miller-Rabin.
    """
    while True:
        # Ensure an odd candidate of the given bit length
        a = (die.randrange(1 << (bits - 1), 1 << bits) << 1) + 1
        if miller_rabin(a):
            return a



#  generate, test, and save primes)

if __name__ == "__main__":
    print("Generating first 1024-bit prime...")
    start_time = time.time()
    p_one = gen_prime(1024)
    end_time = time.time()
    print(f" First prime generated in {round(end_time - start_time, 4)} seconds.\n")

    print("Generating second 1024-bit prime...")
    start_time = time.time()
    p_two = gen_prime(1024)
    end_time = time.time()
    print(f" Second prime generated in {round(end_time - start_time, 4)} seconds.\n")

    # -------------------------------
    # Verify primes with Miller-Rabin
    print(" Testing primality of p_one and p_two...")
    start_time = time.time()
    result_one = miller_rabin(p_one)
    time_one = time.time() - start_time

    start_time = time.time()
    result_two = miller_rabin(p_two)
    time_two = time.time() - start_time

    print(f"p_one is prime: {result_one} (tested in {round(time_one, 4)} seconds)")
    print(f"p_two is prime: {result_two} (tested in {round(time_two, 4)} seconds)\n")

    # -------------------------------
    # Export primes for use in Pollard Rho
    with open("generated_primes.py", "w") as f:
        f.write(f"p_one = {p_one}\n")
        f.write(f"p_two = {p_two}\n")

    # -------------------------------
    # Display the generated primes (formatted)
    print("First 1024-bit prime (p_one):")
    print(p_one, "\n")

    print("Second 1024-bit prime (p_two):")
    print(p_two, "\n")

    print(" Generated primes have been saved to generated_primes.py!")
