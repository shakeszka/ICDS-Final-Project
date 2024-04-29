import random
from sympy import isprime

# generating a random odd integer
def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

# generating a random prime number of specified length
def generate_prime_number(length=1024):
    p = 4
    while not isprime(p):
        p = generate_prime_candidate(length)
    return p

# generating public and private keys
def generate_rsa_keys(keysize):
    # generating two prime numbers
    p = generate_prime_number(keysize // 2)
    q = generate_prime_number(keysize // 2)
    n = p * q

    # calculating Euler's totient function
    phi = (p - 1) * (q - 1)

    # calculating e
    e = 65537
    while phi % e == 0:
        e = generate_prime_number(16)

    # calculating d using bult-in pow function
    d = pow(e, -1, phi)

    # public: (e, n)
    # private: (d, n)
    return ((e, n), (d, n))

# encrypting a message with a public key
def encrypt(message, public_key):
    e, n = public_key
    m = int.from_bytes(message.encode(), 'big') # converting the message to an integer m
    c = pow(m, e, n)
    return c

# decrypting a message with a private key
def decrypt(ciphertext, private_key):
    d, n = private_key
    m = pow(ciphertext, d, n)
    message = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode() # converting the integer message back to string
    return message

def main():
    keysize = 2048  # size of the key
    public_key, private_key = generate_rsa_keys(keysize)
    print("Public Key: (e, n)")
    print(f"e = {public_key[0]}\nn = {public_key[1]}\n")
    print("Private Key: (d, n)")
    print(f"d = {private_key[0]}\nn = {private_key[1]}\n")

    # test
    message = 'Nihao, blyat!'
    print("Original message:", message)
    encrypted_msg = encrypt(message, public_key)
    print("Encrypted message:", encrypted_msg)
    decrypted_msg = decrypt(encrypted_msg, private_key)
    print("Decrypted message:", decrypted_msg)

if __name__ == "__main__":
    main()
