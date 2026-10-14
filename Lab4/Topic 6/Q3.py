from Q1 import naive_mod_exp
from Q2 import binary_mod_exp

tests = [
    (363, 5, 7),
    (363, 10, 13),
    (2, 363, 17),
    (-363, 5, 11),
    (10, 0, 7)
]

for a, b, m in tests:
    naive = naive_mod_exp(a, b, m)
    binary = binary_mod_exp(a, b, m)

    print(f"a={a}, b={b}, m={m}")
    print("Naive:", naive)
    print("Binary:", binary)
    print("Match:", naive == binary)
    print()
