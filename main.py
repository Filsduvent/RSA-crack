
import time
import math
from sympy import isprime


def pollards_rho_factorization(n, max_iterations=10000):
    """
    Pollard's Rho Algorithm for factorization of n.
    :param n: Integer to factorize
    :param max_iterations: Limit on iterations to prevent infinite loops
    :return: A non-trivial factor of n, or None if unsuccessful
    """
    while n < 2:
        print("Invalid input. Please enter an integer greater than 1.")
        try:
            n = int(input("Enter a valid n: "))
        except ValueError:
            print("That's not a valid integer. Try again.")
            continue

    if n % 2 == 0:
        return 2
    
    x, y, d = 2, 2, 1
    f = lambda z: (z**2 + 1) % n  # Function to generate pseudo-random sequence
    iteration = 0
    
    while d == 1 and iteration < max_iterations:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)
        iteration += 1
    
    if d == n:  # Pollard's Rho failed
        print(f"Failed to find a factor for n={n}.")
        return None
    if iteration >= max_iterations:
        print(f"Exceeded maximum iterations for n={n}.")
        return None
    
    return d

def factorize_n(n):
    """Factorize n into two primes p and q."""
    # Handle edge cases where n is too small
    if n < 2:
        raise ValueError("n must be greater than 1")
    
    p = pollards_rho_factorization(n)
    if p is None:
        print("Pollard's Rho failed to factorize n.")
        return None, None

    q = n // p

    # Ensure both p and q are prime and satisfy the factorization
    if isprime(p) and isprime(q) and p * q == n:
        return p, q

    # Handle the case where one of the factors is not prime
    print(f"One or both of the factors found ({p}, {q}) are not prime.")
    return None, None


import math

def modular_inverse(e, phi):
    """Compute the modular inverse of e modulo phi using the Extended Euclidean Algorithm."""
    # Validate that e and phi are coprime
    if math.gcd(e, phi) != 1:
        raise ValueError(f"e and phi must be coprime. gcd({e}, {phi}) != 1")

    # Extended Euclidean Algorithm to find the modular inverse
    x0, x1 = 0, 1
    r0, r1 = phi, e
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
    
    # If r0 != 1, the modular inverse doesn't exist
    if r0 != 1:
        raise ValueError(f"Modular inverse of {e} modulo {phi} does not exist.")
    
    return x0 % phi

def crack_rsa(e, n):
    """Crack RSA to find the private key d."""
    # Step 1: Factorize n
    p, q = factorize_n(n)
    if p is None or q is None:
        raise ValueError("Failed to factorize n into two primes. Ensure n is a product of two primes.")

    # Step 2: Compute phi(n)
    phi = (p - 1) * (q - 1)

    # Step 3: Compute the modular inverse of e mod phi
    d = modular_inverse(e, phi)
    if d is None:
        raise ValueError("Failed to compute the modular inverse of e modulo φ(n).")

    return p, q, d



# Main Program
if __name__ == "__main__":
    while True:
        try:
            # Example usage with input validation
            e = int(input("Enter the public key exponent (e): "))
            n = int(input("Enter the modulus (n): "))

            # Validate the inputs for correct range/format
            if e <= 1 or n <= 1:
                raise ValueError("Both e and n must be greater than 1.")
            
            print("Processing...")
            start = time.time()     
            p, q, d = crack_rsa(e, n)
            end = time.time()

            # Display the results
            print(f"Successfully cracked RSA:")
            print(f"Prime factors: p = {p}, q = {q}")
            print(f"Private key exponent (d): {d}")
            print(f"STATISTIC: Time taken is {end - start:.6f} seconds")

            # Ask if the user wants to continue
            cont = input("Do you want to enter another set of values? (y/n): ").lower()
            if cont != 'y':
                print("Exiting the program.")
                break  # Exit the loop if the user does not want to continue

        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

