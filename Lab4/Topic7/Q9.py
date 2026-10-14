from Q3 import naive_matrix_exp
from Q4 import binary_matrix_exp
import time

matrices = {
    2: [[1, 1], [1, 0]],
    3: [[1, 1, 1], [1, 0, 1], [0, 1, 1]],
    4: [
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1]
    ]
}

for dimension, A in matrices.items():
    for exponent in [363, 3630, 36300]:
        m = 363

        start = time.perf_counter()
        naive_matrix_exp(A, exponent, m)
        naive_time = time.perf_counter() - start

        start = time.perf_counter()
        binary_matrix_exp(A, exponent, m)
        binary_time = time.perf_counter() - start

        print(
            f"Dimension={dimension}, exponent={exponent}, "
            f"naive={naive_time:.6f}s, "
            f"binary={binary_time:.6f}s"
        )
