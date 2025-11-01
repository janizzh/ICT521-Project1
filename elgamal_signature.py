import secrets
from hashlib import sha256

# Parameters
# 1024-bit prime (provided)
p = int("336700791582916887900691338549259095387624169246330866812829299041005206618537620001022107755800801298768580596470705464073798363586363701517920378401778685326197188527455376465761463090193918853013362743946024271708945341501812052910433291788720626650792850657374581631015603747140550324472221219751655617647")

# Choose generator g
g = 2  # (simple choice; not verified primitive root)

# Key Generation
x = secrets.randbelow(p - 2) + 1  # private key
y = pow(g, x, p)                  # public key

# Helper Functions
def hash_message_to_int(msg: bytes, mod: int) -> int:
    """Hash message with SHA-256 and reduce modulo mod."""
    h = sha256(msg).digest()
    return int.from_bytes(h, 'big') % mod

def egcd(a, b):
    if b == 0:
        return (1, 0, a)
    x1, y1, g = egcd(b, a % b)
    return (y1, x1 - (a // b) * y1, g)

def modinv(a, m):
    """Return modular inverse of a mod m."""
    return pow(a, -1, m)

# Signing
def elgamal_sign(message: bytes, p: int, g: int, x: int):
    p_minus_1 = p - 1
    h = hash_message_to_int(message, p_minus_1)

    # choose k coprime to p-1
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    while True:
        k = secrets.randbelow(p_minus_1 - 1) + 1
        if gcd(k, p_minus_1) == 1:
            break

    r = pow(g, k, p)
    inv_k = modinv(k, p_minus_1)
    s = (inv_k * (h - x * r)) % p_minus_1
    return (r, s, h, k)

# Verification
def elgamal_verify(message: bytes, signature: tuple, p: int, g: int, y: int):
    r, s = signature
    if not (1 <= r <= p - 1):
        return False
    p_minus_1 = p - 1
    h = hash_message_to_int(message, p_minus_1)
    left = pow(g, h, p)
    right = (pow(y, r, p) * pow(r, s, p)) % p
    return left == right

# Message containing my name
message_text = "John Smith"  # Replace with your full name
message = message_text.encode()

print("=== ElGamal Signature Test ===")
print("Prime p bits:", p.bit_length())
print("Generator g:", g)
print("Public key y:", y)
print()

# Generate signature
r, s, h, k = elgamal_sign(message, p, g, x)
print("Message:", "Jan Agha Husain")
print("Signature (r, s):")
print(" r =", r)
print(" s =", s)
print("Hash (mod p-1) =", h)
print()

# Verify signature
is_valid = elgamal_verify(message, (r, s), p, g, y)
print("Verification result:", is_valid)

print("\n--- Private Values (for demonstration) ---")
print("Private key x =", x)
print("Random k used =", k)
