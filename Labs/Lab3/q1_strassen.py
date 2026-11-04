"""
Lab 3 - Q1: Matrix Multiplication - Strassen vs Traditional
Divide and Conquer (Notes 4.2)

- Traditional triple-nested-loop multiplication
- Strassen's algorithm (7 recursive multiplications per split)
- Sizes: powers of 2 from 2x2 to 128x128
- Manual or random input (random seed = 292)
- Verifies both results match, counts scalar multiplications, measures time
- Tries base-case cutoffs and reports the fastest
"""

import random
import time

SEED = 292
mult_count = 0          # global counter for scalar multiplications


# ---------------------------------------------------------------- helpers
def random_matrix(n, rng):
    return [[rng.randint(0, 9) for _ in range(n)] for _ in range(n)]


def add(A, B):
    return [[a + b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


def sub(A, B):
    return [[a - b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


def split(M):
    """Split an n x n matrix into four n/2 x n/2 quadrants."""
    h = len(M) // 2
    A11 = [row[:h] for row in M[:h]]
    A12 = [row[h:] for row in M[:h]]
    A21 = [row[:h] for row in M[h:]]
    A22 = [row[h:] for row in M[h:]]
    return A11, A12, A21, A22


def join(C11, C12, C21, C22):
    top = [r1 + r2 for r1, r2 in zip(C11, C12)]
    bottom = [r1 + r2 for r1, r2 in zip(C21, C22)]
    return top + bottom


def print_matrix(M, title):
    print(f"\n{title}:")
    width = max(len(str(x)) for row in M for x in row)
    for row in M:
        print("  " + " ".join(str(x).rjust(width) for x in row))


# ---------------------------------------------------------- traditional
def traditional(A, B):
    """Classic O(n^3) multiplication: exactly n^3 scalar multiplications."""
    global mult_count
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    mult_count += n * n * n
    return C


# ------------------------------------------------------------- strassen
def strassen(A, B, cutoff=1):
    """
    Strassen's algorithm. When n <= cutoff, switch to the traditional
    method. cutoff = 1 means pure Strassen all the way down to 1x1.
    """
    global mult_count
    n = len(A)
    if n <= cutoff:
        return traditional(A, B)

    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)

    M1 = strassen(add(A11, A22), add(B11, B22), cutoff)
    M2 = strassen(add(A21, A22), B11, cutoff)
    M3 = strassen(A11, sub(B12, B22), cutoff)
    M4 = strassen(A22, sub(B21, B11), cutoff)
    M5 = strassen(add(A11, A12), B22, cutoff)
    M6 = strassen(sub(A21, A11), add(B11, B12), cutoff)
    M7 = strassen(sub(A12, A22), add(B21, B22), cutoff)

    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(sub(add(M1, M3), M2), M6)
    return join(C11, C12, C21, C22)


# ------------------------------------------------------------- runners
def run_once(A, B, method, cutoff=1):
    global mult_count
    mult_count = 0
    t0 = time.perf_counter()
    C = traditional(A, B) if method == "trad" else strassen(A, B, cutoff)
    t = time.perf_counter() - t0
    return C, mult_count, t


def read_matrix(n, name):
    print(f"Enter matrix {name} ({n}x{n}), one row per line, values separated by spaces:")
    M = []
    for i in range(n):
        while True:
            parts = input(f"  row {i + 1}: ").split()
            if len(parts) == n:
                try:
                    M.append([int(x) for x in parts])
                    break
                except ValueError:
                    pass
            print(f"  Please enter exactly {n} integers.")
    return M


def manual_demo():
    while True:
        try:
            n = int(input("Matrix size (power of 2, e.g. 2, 4, 8): "))
            if n >= 1 and (n & (n - 1)) == 0:
                break
        except ValueError:
            pass
        print("Size must be a power of 2.")
    A = read_matrix(n, "A")
    B = read_matrix(n, "B")
    show_single(A, B)


def show_single(A, B):
    C1, m1, t1 = run_once(A, B, "trad")
    C2, m2, t2 = run_once(A, B, "strassen", cutoff=1)
    print_matrix(A, "Matrix A")
    print_matrix(B, "Matrix B")
    print_matrix(C1, "Result (Traditional)")
    print_matrix(C2, "Result (Strassen)")
    print(f"\nResults match: {C1 == C2}")
    print(f"Traditional: {m1} multiplications, {t1 * 1000:.4f} ms")
    print(f"Strassen   : {m2} multiplications, {t2 * 1000:.4f} ms")


def benchmark():
    rng = random.Random(SEED)
    sizes = [2, 4, 8, 16, 32, 64, 128]

    # Show a small example in full
    A = random_matrix(4, rng)
    B = random_matrix(4, rng)
    print("=" * 70)
    print(f"Example with random 4x4 matrices (seed = {SEED})")
    print("=" * 70)
    show_single(A, B)

    print("\n" + "=" * 86)
    print("Traditional vs pure Strassen (cutoff = 1)")
    print("=" * 86)
    print(f"{'n':>5} | {'Trad mults':>12} | {'Trad time(s)':>12} | "
          f"{'Strassen mults':>14} | {'Strassen time(s)':>16} | {'Match':>5}")
    print("-" * 86)
    matrices = {}
    for n in sizes:
        A = random_matrix(n, rng)
        B = random_matrix(n, rng)
        matrices[n] = (A, B)
        C1, m1, t1 = run_once(A, B, "trad")
        C2, m2, t2 = run_once(A, B, "strassen", cutoff=1)
        print(f"{n:>5} | {m1:>12,} | {t1:>12.5f} | {m2:>14,} | {t2:>16.5f} | "
              f"{str(C1 == C2):>5}")
    print("\nTheory: traditional = n^3,  pure Strassen = 7^log2(n) = n^2.807")

    # Cutoff experiment
    n = 128
    A, B = matrices[n]
    C_ref, _, _ = run_once(A, B, "trad")
    print("\n" + "=" * 70)
    print(f"Base-case cutoff experiment for n = {n}")
    print("(use traditional when sub-matrix size <= cutoff)")
    print("=" * 70)
    print(f"{'cutoff':>7} | {'mults':>12} | {'time(s)':>10} | {'Match':>5}")
    print("-" * 46)
    best = None
    for cutoff in [1, 2, 4, 8, 16, 32, 64, 128]:
        C, m, t = run_once(A, B, "strassen", cutoff)
        print(f"{cutoff:>7} | {m:>12,} | {t:>10.5f} | {str(C == C_ref):>5}")
        if best is None or t < best[1]:
            best = (cutoff, t)
    print(f"\nFastest cutoff: {best[0]} ({best[1]:.5f} s)")
    print("Note: cutoff = 128 is just the traditional method.")
    print("Below a certain size, Strassen's extra additions and list copying cost")
    print("more than the multiplications it saves, so a hybrid cutoff wins.")


def main():
    print("Lab 3 Q1 - Strassen vs Traditional Matrix Multiplication")
    print("1. Enter matrices manually")
    print("2. Generate random matrices and run full benchmark (seed 292)")
    choice = input("Choose 1 or 2: ").strip()
    if choice == "1":
        manual_demo()
    else:
        benchmark()


if __name__ == "__main__":
    main()
