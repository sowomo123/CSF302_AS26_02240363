from Q2 import binary_mod_exp

try:
    a = int(input("Enter base: "))
    b = int(input("Enter exponent: "))
    m = int(input("Enter positive modulus: "))

    print("Result:", binary_mod_exp(a, b, m))

except ValueError as error:
    print("Invalid input:", error)
