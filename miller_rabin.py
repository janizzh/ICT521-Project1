# This code implements Miller-Rabin primality test algorithm that checks if a number is prime, by checking if n is divisible by one of the terms in the algorithm, then n probably is prime.
# We check a number n for primeness, take a random number a between 1 and n - 1, and check if n is divisible by one of the terms in the formula / algorithm.

import random
die = random.SystemRandom() # A single dice

def single_test(n, a): # take number n and test it for primeness, and a is the witness
   exp = n -1
   while not exp & 1: # While exp is not even
       exp >>= 1 # bit manipulation, cut off the right bit, same as exp // 2 (integer division by 2), but since n is going to be large, bit-wise operations would be faster when dealing with integers


   if pow(a, exp, n) == 1:
       return True

   while exp < n - 1:
       if pow(a, exp, n) == n - 1:
           return True

       exp <<= 1

   return False # If none of the terms above are divisible by n, return False


def miller_rabin(n, k=40): # k is the values of a, choosing 40 lowers the chance of being wrong about the assumption of n being a prime
    for i in range(k): # Check for k values
        a = die.randrange(2, n - 1) # Random number greater than two, lower than n - 1 ( 1 < a < n - 1 ) for value of a
        if not single_test(n, a):
            return False # If not verified as prime by the test, return False, if a number is not Prime then it must be Composite

    return True # Otherwise return True

#print(miller_rabin(4)) # Print if  a certain number is Prime or not, output is either True or False.

def gen_prime(bits): # Function that will generate prime with bits number of bits, by generating large odd numbers and check if its prime
    while True:
        a = (die.randrange(1 << bits - 1, 1 << bits) << 1) + 1 # Generates a large prime with specified number of bits, guarantees that a is odd
        if miller_rabin(a):
            return a



# Generate two 1024 bit prime numbers, to check for primeness either, paste the output i.eg. the prime number, above in the code at:
# print(miller_rabin(4), remove the comment # and replace 4 with the 1024-bit number that was generated, and it will give you either True or False, if it is prime or not.
# One can also multiply p_one and p_two to check for primeness, if the two numbers are prime, the result of their multiplication will always be a non prime / composite number.
# You will have to use either ChatGPT, Wolfram Alpha or any third party tool to confirm if the resulted number after multiplication is prime or not as my code does not include that.
p_one = gen_prime(1024)
p_two = gen_prime(1024)

# After generating the two 1024-bit prime numbers, remember to comment the above and below code out, such that when you check for primeness, you don't generate new prime numbers.

print(p_one) # prints the first 1024-bit prime number
print(p_two) # prints the second 1024-bit prime number

#print(p_one * p_two) # Multiplication method
# If you want to use the multiplication method, remove the comment # and run the code for the results, and check with a third party tool if the resulted number is prime or not


