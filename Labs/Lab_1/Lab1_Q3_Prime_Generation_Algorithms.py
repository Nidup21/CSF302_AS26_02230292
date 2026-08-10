import time
import math

def naive_trial_division(n):
    """Return list of primes up to n using naive trial division."""
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for d in range(2, num):
            if num % d == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

def optimized_trial_division(n):
    """Return list of primes up to n using trial division up to sqrt(num)."""
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        limit = int(math.isqrt(num))
        for d in range(2, limit + 1):
            if num % d == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

def sieve_of_eratosthenes(n):
    """Return list of primes up to n using Sieve of Eratosthenes."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start:n+1:step] = [False] * ((n - start) // step + 1)
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def measure_prime_time(func, n):
    """Measure time to generate primes up to n (single run)."""
    start = time.perf_counter()
    func(n)
    end = time.perf_counter()
    return end - start

def main():
    sizes = [10000, 50000, 100000, 500000, 1000000]
    results = []

    for n in sizes:
        # Naive (skip for large n because it's too slow)
        if n <= 10000:
            naive_time = measure_prime_time(naive_trial_division, n)
        else:
            naive_time = float('inf')  # mark as too slow

        opt_time = measure_prime_time(optimized_trial_division, n)
        sieve_time = measure_prime_time(sieve_of_eratosthenes, n)

        results.append((n, naive_time, opt_time, sieve_time))
        print(f"N={n}: Naive={naive_time:.4f}s, Optimized={opt_time:.4f}s, Sieve={sieve_time:.4f}s")

    # Write results to Results.md
    with open("Results.md", "a") as f:
        f.write("\n## Question 3: Prime Generation Algorithms\n")
        f.write("| N | Naive Trial (s) | Optimized Trial (s) | Sieve of Eratosthenes (s) |\n")
        f.write("|---|----------------|---------------------|---------------------------|\n")
        for n, naive, opt, sieve in results:
            naive_str = f"{naive:.4f}" if naive != float('inf') else "N/A"
            f.write(f"| {n} | {naive_str} | {opt:.4f} | {sieve:.4f} |\n")

if __name__ == "__main__":
    main()