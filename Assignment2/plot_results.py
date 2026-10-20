import csv
import math
import matplotlib.pyplot as plt

sizes = []
brute_times = []
divide_times = []

with open("timing_results.csv", newline="") as file:
    for row in csv.DictReader(file):
        n = int(row["n"])
        divide = float(row["divide_seconds"])
        brute = row["brute_seconds"]
        sizes.append(n)
        divide_times.append(divide)
        if brute.strip() and brute.strip().lower() != "none" and brute.strip() != "stopped" and brute.strip() != "skipped":
            brute_times.append((n, float(brute)))

plt.figure(figsize=(9, 6))
plt.loglog(
    sizes, divide_times,
    marker="o", label="Divide and conquer")
if brute_times:
    bx, by = zip(*brute_times)
    plt.loglog(bx, by, marker="s", label="Brute force")
plt.xlabel("Number of points (n)")
plt.ylabel("Execution time (seconds)")
plt.title("Closest Pair Algorithms: Log-Log Performance")
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend()
plt.savefig("timing_graph.png", dpi=150, bbox_inches="tight")
print("Saved timing_graph.png")
