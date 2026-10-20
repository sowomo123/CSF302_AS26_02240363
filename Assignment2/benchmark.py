import csv
import math
import multiprocessing as mp
import random
import time
from closest import closest_pair, closest_pair_brute

SIZES = [1000, 2000, 4000, 8000, 16000, 32000, 64000]
BRUTE_LIMIT_SECONDS = 60


def run_brute(points, queue):
    start = time.perf_counter()
    closest_pair_brute(points)
    queue.put(time.perf_counter() - start)


def timed_brute(points, timeout=BRUTE_LIMIT_SECONDS):
    # A separate process lets us stop a long brute-force run.
    ctx = mp.get_context("spawn")
    queue = ctx.Queue()
    process = ctx.Process(target=run_brute, args=(points, queue))
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join()
        queue.close()
        queue.join_thread()
        return None
    try:
        elapsed = queue.get(timeout=2)
    except Exception:
        queue.close()
        queue.join_thread()
        return None
    return elapsed


def timed_divide(points):
    start = time.perf_counter()
    closest_pair(points)
    return time.perf_counter() - start


def main():
    rng = random.Random(2026)
    results = []
    brute_allowed = True

    for n in SIZES:
        points = [
            (rng.uniform(-1000, 1000), rng.uniform(-1000, 1000))
            for _ in range(n)
        ]

        divide_time = timed_divide(points)

        if brute_allowed:
            brute_time = timed_brute(points)
            if brute_time is None:
                brute_time = "stopped"
                brute_allowed = False
        else:
            brute_time = "skipped"

        results.append({
            "n": n,
            "brute_seconds": brute_time,
            "divide_seconds": divide_time
        })

        brute_str = brute_time if isinstance(brute_time, str) else f"{brute_time:.6f}"
        print(f"n={n:6d} | brute={brute_str:>10s} | divide={divide_time:.6f} s")

    with open("timing_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "brute_seconds", "divide_seconds"])
        writer.writeheader()
        writer.writerows(results)

    print("\nSaved timing_results.csv")

    # Find crossover point
    crossover = None
    for r in results:
        if r["brute_seconds"] not in ["stopped", "skipped"]:
            if float(r["brute_seconds"]) > r["divide_seconds"]:
                crossover = r["n"]
                break

    if crossover:
        print(f"First tested crossover size: n = {crossover}")
    else:
        print("No crossover observed in completed measurements")


if __name__ == "__main__":
    main()
