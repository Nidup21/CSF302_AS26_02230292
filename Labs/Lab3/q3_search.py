"""
Lab 3 - Q3: Binary Search vs Ternary Search (menu-driven)
Divide and Conquer (Notes 4.5)

Comparisons counted per round (key-to-element comparisons):
  Binary  : 2 per round  (a[mid] == key, key < a[mid])          T(n) = T(n/2) + 2
  Ternary : 4 per round  (== a[m1], == a[m2], < a[m1], > a[m2])  T(n) = T(n/3) + 4
Random seed = 292, default n = 292.
"""

import math
import random

SEED = 292
DEFAULT_N = 292


# ---------------------------------------------------------------- data
def generate_sorted(n, seed=SEED):
    """n distinct sorted random integers."""
    rng = random.Random(seed)
    return sorted(rng.sample(range(1, 10 * n + 1), n))


# ------------------------------------------------------------ searches
def binary_search(a, key):
    lo, hi, comps = 0, len(a) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comps += 1
        if a[mid] == key:
            return mid, comps
        comps += 1
        if key < a[mid]:
            hi = mid - 1
        else:
            lo = mid + 1
    return -1, comps


def ternary_search(a, key):
    lo, hi, comps = 0, len(a) - 1, 0
    while lo <= hi:
        third = (hi - lo) // 3
        m1, m2 = lo + third, hi - third
        comps += 1
        if a[m1] == key:
            return m1, comps
        comps += 1
        if a[m2] == key:
            return m2, comps
        comps += 1
        if key < a[m1]:
            hi = m1 - 1
        else:
            comps += 1
            if key > a[m2]:
                lo = m2 + 1
            else:
                lo, hi = m1 + 1, m2 - 1
    return -1, comps


# --------------------------------------------------------- case helpers
def best_case(a):
    """Key sits at the first probe position -> 1 comparison."""
    n = len(a)
    b_key = a[(n - 1) // 2]
    t_key = a[(n - 1) // 3]
    return b_key, binary_search(a, b_key)[1], t_key, ternary_search(a, t_key)[1]


def worst_case(a):
    """Key absent and larger than every element -> search goes the full depth,
    and ternary pays all 4 comparisons in every round."""
    key = a[-1] + 1
    return key, binary_search(a, key)[1], ternary_search(a, key)[1]


# --------------------------------------------------------------- menu
def show_array(a):
    if not a:
        print("Array is empty. Generate it first (option 1).")
        return
    print(f"Array (n = {len(a)}):")
    if len(a) <= 300:
        for i in range(0, len(a), 15):
            print("  " + " ".join(f"{x:5d}" for x in a[i:i + 15]))
    else:
        print("  first 20:", a[:20])
        print("  last 20 :", a[-20:])


def read_int(prompt, default=None):
    while True:
        s = input(prompt).strip()
        if s == "" and default is not None:
            return default
        try:
            return int(s)
        except ValueError:
            print("Please enter an integer.")


def do_search(a, which):
    if not a:
        print("Array is empty. Generate it first (option 1).")
        return
    key = read_int(f"Enter key to search [default {DEFAULT_N}]: ", DEFAULT_N)
    fn = binary_search if which == "binary" else ternary_search
    idx, comps = fn(a, key)
    name = "Binary" if which == "binary" else "Ternary"
    if idx >= 0:
        print(f"{name} Search: key {key} found at index {idx} after {comps} comparisons.")
    else:
        print(f"{name} Search: key {key} NOT found after {comps} comparisons.")


def comparison_table():
    print(f"\n{'n':>8} | {'Bin best':>8} | {'Tern best':>9} | {'Bin worst':>9} | "
          f"{'Tern worst':>10} | {'2*log2(n)':>9} | {'4*log3(n)':>9}")
    print("-" * 80)
    for n in [10, 100, 1_000, 10_000, 100_000]:
        a = generate_sorted(n)
        _, bb, _, tb = best_case(a)
        _, bw, tw = worst_case(a)
        print(f"{n:>8,} | {bb:>8} | {tb:>9} | {bw:>9} | {tw:>10} | "
              f"{2 * math.log2(n):>9.1f} | {4 * math.log(n, 3):>9.1f}")
    print("\nTernary search makes MORE comparisons in the worst case than binary search.")


def explain():
    print("""
Explanation using the recurrences
---------------------------------
Binary search: each round does 2 comparisons and keeps 1/2 of the array.
    T(n) = T(n/2) + 2   ->   T(n) = 2 log2(n)

Ternary search: each round does up to 4 comparisons and keeps 1/3 of the array.
    T(n) = T(n/3) + 4   ->   T(n) = 4 log3(n)

Compare them:
    4 log3(n) = 4 * log2(n) / log2(3) = (4 / 1.585) log2(n) = 2.52 log2(n)

So ternary search does about 2.52 log2(n) comparisons versus 2 log2(n) for
binary search: roughly 26% more. Ternary search needs fewer rounds
(log3 n < log2 n) but pays double the comparisons per round, and the saving
in rounds (factor log2 3 = 1.585) is smaller than the extra cost (factor 2).

Both are O(log n), but binary search has the smaller constant, which is
exactly what the comparison table (option 7) shows. Best case for both is
1 comparison, when the key sits at the first probe position.
""")


def main():
    a = []
    while True:
        print("\n===== Binary vs Ternary Search =====")
        print("1. Generate n sorted random numbers")
        print("2. Display the array")
        print("3. Search for a key using Binary Search")
        print("4. Search for a key using Ternary Search")
        print("5. Comparison count for the best case")
        print("6. Comparison count for the worst case (key absent)")
        print("7. Comparison count table for n = 10, 100, ..., 100,000")
        print("8. Explain the result using the recurrences")
        print("0. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            n = read_int(f"Enter n [default {DEFAULT_N}]: ", DEFAULT_N)
            if n <= 0:
                print("n must be positive.")
                continue
            a = generate_sorted(n)
            print(f"Generated {n} sorted random numbers (seed {SEED}).")
        elif choice == "2":
            show_array(a)
        elif choice == "3":
            do_search(a, "binary")
        elif choice == "4":
            do_search(a, "ternary")
        elif choice == "5":
            if not a:
                print("Array is empty. Generate it first (option 1).")
                continue
            bk, bc, tk, tc = best_case(a)
            print(f"Best case (n = {len(a)}):")
            print(f"  Binary : key {bk} at middle      -> {bc} comparison(s)")
            print(f"  Ternary: key {tk} at first third -> {tc} comparison(s)")
        elif choice == "6":
            if not a:
                print("Array is empty. Generate it first (option 1).")
                continue
            k, bc, tc = worst_case(a)
            print(f"Worst case, key {k} absent (n = {len(a)}):")
            print(f"  Binary : {bc} comparisons  (theory 2*log2(n) = {2 * math.log2(len(a)):.1f})")
            print(f"  Ternary: {tc} comparisons  (theory 4*log3(n) = {4 * math.log(len(a), 3):.1f})")
        elif choice == "7":
            comparison_table()
        elif choice == "8":
            explain()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
