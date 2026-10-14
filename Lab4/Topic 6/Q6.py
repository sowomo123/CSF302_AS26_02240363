from Q1 import naive_mod_exp
from Q2 import binary_mod_exp
import time

print("Exponent | Naive time | Binary time")

for exponent in [363, 3630, 36300, 363000]:
    start = time.perf_counter()
    naive_mod_exp(2, exponent, 1009)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    binary_mod_exp(2, exponent, 1009)
    binary_time = time.perf_counter() - start

    print(
        exponent,
        f"{naive_time:.6f}s",
        f"{binary_time:.6f}s"
    )
