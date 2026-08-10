import random
import time

def bubble_sort(arr):
    """In-place bubble sort."""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def merge_sort(arr):
    """Merge sort (returns new sorted list)."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def measure_sort_time(sort_func, arr):
    """Measure time for one sort run (use copy to avoid in-place side effects)."""
    # For bubble sort we need a copy because it modifies in-place
    arr_copy = arr[:]
    start = time.perf_counter()
    if sort_func.__name__ == "bubble_sort":
        sort_func(arr_copy)          # in-place
    else:
        arr_copy = sort_func(arr_copy)  # returns new list
    end = time.perf_counter()
    return end - start

def main():
    sizes = [100, 500, 1000, 2000, 4000, 8000]
    results = []

    for size in sizes:
        # Generate random array of integers
        data = [random.randint(0, 10000) for _ in range(size)]

        # Bubble sort (average over 3 runs for stability)
        bubble_times = [measure_sort_time(bubble_sort, data) for _ in range(3)]
        avg_bubble = sum(bubble_times) / len(bubble_times)

        # Merge sort (average over 3 runs)
        merge_times = [measure_sort_time(merge_sort, data) for _ in range(3)]
        avg_merge = sum(merge_times) / len(merge_times)

        results.append((size, avg_bubble, avg_merge))
        print(f"Size {size}: Bubble = {avg_bubble:.6f}s, Merge = {avg_merge:.6f}s")

    # Write results to Results.md
    with open("Results.md", "a") as f:
        f.write("\n## Question 2: Bubble Sort vs Merge Sort\n")
        f.write("| Input Size | Bubble Sort (avg s) | Merge Sort (avg s) |\n")
        f.write("|------------|---------------------|--------------------|\n")
        for size, bub, mer in results:
            f.write(f"| {size} | {bub:.6f} | {mer:.6f} |\n")

if __name__ == "__main__":
    main()