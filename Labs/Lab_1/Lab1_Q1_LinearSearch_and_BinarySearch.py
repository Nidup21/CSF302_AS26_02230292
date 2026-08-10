import random
import time
import bisect

def linear_search(arr, target):
    """Return index of target if found, else -1."""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def binary_search(arr, target):
    """Return index of target if found, else -1 using iterative binary search."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def measure_search_time(search_func, arr, target, is_sorted=False):
    """Measure average time of search_func over 10 runs."""
    times = []
    for _ in range(10):
        # If using binary search, the array must be sorted (already sorted outside)
        start = time.perf_counter()
        search_func(arr, target)
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times)

def main():
    sizes = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    results = []

    for size in sizes:
        # Generate random dataset of integers between 0 and size*10
        data = [random.randint(0, size * 10) for _ in range(size)]
        target = random.choice(data)  # guarantee target exists

        # Linear search on unsorted data
        lin_time = measure_search_time(linear_search, data, target, is_sorted=False)

        # Sort for binary search
        sorted_data = sorted(data)
        bin_time = measure_search_time(binary_search, sorted_data, target, is_sorted=True)

        results.append((size, lin_time, bin_time))
        print(f"Size {size}: Linear = {lin_time:.6f}s, Binary = {bin_time:.6f}s")

    # Write results to Results.md (append)
    with open("Results.md", "a") as f:
        f.write("\n## Question 1: Linear Search vs Binary Search\n")
        f.write("| Input Size | Linear Search (avg s) | Binary Search (avg s) |\n")
        f.write("|------------|-----------------------|-----------------------|\n")
        for size, lin, bin_ in results:
            f.write(f"| {size} | {lin:.6f} | {bin_:.6f} |\n")

if __name__ == "__main__":
    main()