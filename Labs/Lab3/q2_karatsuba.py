"""
Lab 3 - Q2: Karatsuba Large Integer Multiplication
Divide and Conquer (Notes 4.3)

- Integers stored as digit strings (no native size limit)
- Traditional grade-school multiplication
- Karatsuba (3 recursive multiplications per split)
- Both operands padded to the same length in every recursive call
- Base case: 4 digits (uses grade-school)
- Sizes 8, 16, 32, ..., 1024 digits; manual or random input (seed = 292)
- Verifies Karatsuba == traditional, counts digit multiplications, times both
"""

import random
import time

SEED = 292
BASE_CASE = 4
digit_mults = 0      # global counter of single-digit multiplications


# ------------------------------------------------------- string helpers
def strip(s):
    s = s.lstrip("0")
    return s if s else "0"


def add_str(a, b):
    """Add two non-negative digit strings."""
    i, j, carry, out = len(a) - 1, len(b) - 1, 0, []
    while i >= 0 or j >= 0 or carry:
        d = carry
        if i >= 0:
            d += ord(a[i]) - 48
            i -= 1
        if j >= 0:
            d += ord(b[j]) - 48
            j -= 1
        out.append(chr(d % 10 + 48))
        carry = d // 10
    return strip("".join(reversed(out)))


def sub_str(a, b):
    """a - b for digit strings, assumes a >= b."""
    i, j, borrow, out = len(a) - 1, len(b) - 1, 0, []
    while i >= 0:
        d = ord(a[i]) - 48 - borrow
        if j >= 0:
            d -= ord(b[j]) - 48
            j -= 1
        if d < 0:
            d += 10
            borrow = 1
        else:
            borrow = 0
        out.append(chr(d + 48))
        i -= 1
    return strip("".join(reversed(out)))


def shift(s, k):
    """Multiply by 10^k."""
    return s + "0" * k if s != "0" else "0"


# --------------------------------------------------------- grade school
def grade_school(x, y):
    """Classic long multiplication: len(x) * len(y) digit multiplications."""
    global digit_mults
    a = [ord(c) - 48 for c in reversed(x)]
    b = [ord(c) - 48 for c in reversed(y)]
    res = [0] * (len(a) + len(b))
    for i, da in enumerate(a):
        carry = 0
        for j, db in enumerate(b):
            cur = res[i + j] + da * db + carry
            res[i + j] = cur % 10
            carry = cur // 10
        k = i + len(b)
        while carry:
            cur = res[k] + carry
            res[k] = cur % 10
            carry = cur // 10
            k += 1
    digit_mults += len(a) * len(b)
    return strip("".join(str(d) for d in reversed(res)))


# ------------------------------------------------------------ karatsuba
def karatsuba(x, y):
    # Pad both operands to the same length (x0 + x1 may have an extra digit)
    n = max(len(x), len(y))
    x, y = x.zfill(n), y.zfill(n)

    if n <= BASE_CASE:
        return grade_school(x, y)

    if n % 2:                       # make length even for a clean split
        n += 1
        x, y = x.zfill(n), y.zfill(n)

    m = n // 2                      # number of low digits
    x1, x0 = x[:m], x[m:]
    y1, y0 = y[:m], y[m:]

    z2 = karatsuba(x1, y1)                                  # high * high
    z0 = karatsuba(x0, y0)                                  # low * low
    z1 = karatsuba(add_str(x1, x0), add_str(y1, y0))        # (x1+x0)(y1+y0)
    middle = sub_str(sub_str(z1, z2), z0)                   # x1*y0 + x0*y1

    return add_str(add_str(shift(z2, 2 * m), shift(middle, m)), z0)


# --------------------------------------------------------------- driver
def random_number(digits, rng):
    return str(rng.randint(1, 9)) + "".join(str(rng.randint(0, 9)) for _ in range(digits - 1))


def run(fn, x, y):
    global digit_mults
    digit_mults = 0
    t0 = time.perf_counter()
    r = fn(x, y)
    return r, digit_mults, time.perf_counter() - t0


def compare(x, y, show=True):
    r1, m1, t1 = run(grade_school, x, y)
    r2, m2, t2 = run(karatsuba, x, y)
    if show:
        print(f"\nX = {x}")
        print(f"Y = {y}")
        print(f"Traditional : {r1}")
        print(f"Karatsuba   : {r2}")
        print(f"Match       : {r1 == r2}  (Python check: {int(r1) == int(x) * int(y)})")
        print(f"Digit mults : traditional = {m1}, karatsuba = {m2}")
        print(f"Time        : traditional = {t1 * 1000:.4f} ms, karatsuba = {t2 * 1000:.4f} ms")
    return r1, m1, t1, r2, m2, t2


def read_number(name):
    while True:
        s = input(f"Enter {name} (digits only): ").strip()
        if s.isdigit():
            return strip(s)
        print("Please enter a non-negative integer.")


def benchmark():
    rng = random.Random(SEED)

    print("=" * 70)
    print(f"Example: 292 x 292 and a random 8-digit pair (seed = {SEED})")
    print("=" * 70)
    compare("292", "292")
    compare(random_number(8, rng), random_number(8, rng))

    print("\n" + "=" * 92)
    print("Grade-school vs Karatsuba (base case = 4 digits)")
    print("=" * 92)
    print(f"{'digits':>6} | {'Trad mults':>11} | {'Trad time(s)':>12} | "
          f"{'Kara mults':>11} | {'Kara time(s)':>12} | {'Ratio':>6} | {'Match':>5}")
    print("-" * 92)
    for n in [8, 16, 32, 64, 128, 256, 512, 1024]:
        x, y = random_number(n, rng), random_number(n, rng)
        r1, m1, t1, r2, m2, t2 = compare(x, y, show=False)
        ok = (r1 == r2) and int(r1) == int(x) * int(y)
        print(f"{n:>6} | {m1:>11,} | {t1:>12.5f} | {m2:>11,} | {t2:>12.5f} | "
              f"{m1 / m2:>6.2f} | {str(ok):>5}")
    print("\nTheory: grade-school = n^2 digit multiplications,")
    print("        Karatsuba    = T(n) = 3T(n/2) + O(n)  ->  O(n^log2(3)) = O(n^1.585)")
    print("Each doubling of n multiplies traditional mults by 4, Karatsuba by about 3.")


def main():
    print("Lab 3 Q2 - Karatsuba Large Integer Multiplication")
    print("1. Enter two numbers manually")
    print("2. Generate random numbers and run full benchmark (seed 292)")
    choice = input("Choose 1 or 2: ").strip()
    if choice == "1":
        x = read_number("first number")
        y = read_number("second number")
        compare(x, y)
    else:
        benchmark()


if __name__ == "__main__":
    main()
