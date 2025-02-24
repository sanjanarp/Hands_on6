import random
import time
import matplotlib.pyplot as plt
import sys

# Increase recursion limit to handle deep recursions for larger inputs
sys.setrecursionlimit(10000)

#########################################
# 1. Quicksort Implementations
#########################################

def quicksort_non_random(arr):
    """
    Standard quicksort using the non-random pivot.
    The pivot is always chosen as the first element.
    """
    if len(arr) <= 1:
        return arr  # Base case: array with 0 or 1 element is already sorted.
    pivot = arr[0]
    # Partition into two lists: one with elements less than the pivot and one with the rest.
    less = [x for x in arr[1:] if x < pivot]
    greater = [x for x in arr[1:] if x >= pivot]
    # Recursively sort partitions and combine them with the pivot.
    return quicksort_non_random(less) + [pivot] + quicksort_non_random(greater)

def quicksort_random(arr):
    """
    Standard quicksort using a random pivot.
    A random index is chosen, its element is swapped with the first element,
    and then the partitioning continues.
    """
    if len(arr) <= 1:
        return arr  # Base case.
    # Choose a random pivot index and swap the element with the first element.
    pivot_index = random.randint(0, len(arr) - 1)
    arr[0], arr[pivot_index] = arr[pivot_index], arr[0]
    pivot = arr[0]
    # Partition the remaining elements.
    less = [x for x in arr[1:] if x < pivot]
    greater = [x for x in arr[1:] if x >= pivot]
    # Recursively sort and combine.
    return quicksort_random(less) + [pivot] + quicksort_random(greater)

#########################################
# 2. Debug Versions (Show Internal Working)
#########################################

def quicksort_non_random_debug(arr, depth=0):
    """
    Debug version of non-random pivot quicksort.
    Prints the pivot chosen and the partitions at each recursion level.
    """
    indent = '  ' * depth  # Indentation to illustrate recursion depth.
    if len(arr) <= 1:
        print(indent + f"Base case reached: {arr}")
        return arr
    pivot = arr[0]
    print(indent + f"Non-random pivot: {pivot} from {arr}")
    less = [x for x in arr[1:] if x < pivot]
    greater = [x for x in arr[1:] if x >= pivot]
    print(indent + f"Partitioned into -> less: {less}, greater: {greater}")
    sorted_less = quicksort_non_random_debug(less, depth + 1)
    sorted_greater = quicksort_non_random_debug(greater, depth + 1)
    return sorted_less + [pivot] + sorted_greater

def quicksort_random_debug(arr, depth=0):
    """
    Debug version of random pivot quicksort.
    Prints the randomly chosen pivot and the partitions at each recursion level.
    """
    indent = '  ' * depth
    if len(arr) <= 1:
        print(indent + f"Base case reached: {arr}")
        return arr
    pivot_index = random.randint(0, len(arr) - 1)
    arr[0], arr[pivot_index] = arr[pivot_index], arr[0]
    pivot = arr[0]
    print(indent + f"Random pivot chosen: {pivot} from {arr}")
    less = [x for x in arr[1:] if x < pivot]
    greater = [x for x in arr[1:] if x >= pivot]
    print(indent + f"Partitioned into -> less: {less}, greater: {greater}")
    sorted_less = quicksort_random_debug(less, depth + 1)
    sorted_greater = quicksort_random_debug(greater, depth + 1)
    return sorted_less + [pivot] + sorted_greater

#########################################
# 3. Input Generators for Benchmarking
#########################################

def generate_best_case(arr):
    """
    Generates an input ordering for the best-case scenario of non-random quicksort.
    In this case, the pivot (first element) is always the median,
    resulting in balanced partitions.
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2  # Median index.
    # Place the median first, then recursively do the same for left and right subarrays.
    return [arr[mid]] + generate_best_case(arr[:mid]) + generate_best_case(arr[mid+1:])

def generate_worst_case(n):
    """
    Generates the worst-case input for non-random quicksort.
    For a fixed pivot (first element), a sorted array is worst-case.
    """
    return list(range(n))

def generate_average_case(n):
    """
    Generates an average-case input for quicksort.
    Returns an array of 'n' random integers from a uniform distribution.
    """
    return [random.randint(0, n) for _ in range(n)]

#########################################
# 4. Benchmarking Code
#########################################

def benchmark_quicksort(sort_func, input_generator, sizes, trials=3):
    """
    Benchmarks the provided quicksort function using the given input generator.
    
    Parameters:
      - sort_func: The quicksort function to benchmark.
      - input_generator: Function that generates an input array of size 'n'.
      - sizes: List of input sizes.
      - trials: Number of trials to average the running time.
      
    Returns:
      - List of average execution times for each input size.
    """
    times = []
    for n in sizes:
        total_time = 0
        for _ in range(trials):
            arr = input_generator(n)
            start = time.time()
            sort_func(arr)
            total_time += time.time() - start
        times.append(total_time / trials)
    return times

#########################################
# 5. Test Cases for Both Implementations
#########################################

def test_quicksort():
    """
    Tests both quicksort implementations (non-random and random pivot)
    against several test cases to verify correctness.
    """
    test_arrays = [
        [],                             # Empty list.
        [1],                            # Single element.
        [2, 1],                         # Two elements.
        [1, 2, 3, 4, 5],                # Already sorted.
        [5, 4, 3, 2, 1],                # Reverse sorted.
        [3, 1, 2, 1, 5, 3],             # Contains duplicates.
        [random.randint(0, 100) for _ in range(10)]  # Random list.
    ]
    
    for arr in test_arrays:
        expected = sorted(arr)  # Expected result using Python's built-in sorted().
        result_non_random = quicksort_non_random(arr.copy())
        result_random = quicksort_random(arr.copy())
        print("Original array:     ", arr)
        print("Expected sorted:    ", expected)
        print("Non-random result:  ", result_non_random)
        print("Random pivot result:", result_random)
        print("-" * 50)
        assert result_non_random == expected, "Non-random quicksort failed!"
        assert result_random == expected, "Random pivot quicksort failed!"
    
    print("All quicksort tests passed!")

#########################################
# 6. Main Execution Block
#########################################

if __name__ == '__main__':
    # Run test cases for both quicksort implementations.
    print("----- Running Quicksort Test Cases -----")
    test_quicksort()
    
    # Demonstrate debug versions to show how the two implementations differ.
    test_array = [3, 6, 1, 8, 2, 5]
    print("\n----- Debugging Non-Random Quicksort -----")
    sorted_non_random_debug = quicksort_non_random_debug(test_array.copy())
    print("Sorted result (Non-Random):", sorted_non_random_debug)
    
    print("\n----- Debugging Random Pivot Quicksort -----")
    sorted_random_debug = quicksort_random_debug(test_array.copy())
    print("Sorted result (Random Pivot):", sorted_random_debug)
    
    # Define input sizes for benchmarking the non-random quicksort.
    sizes = [100, 200, 500, 1000, 2000, 5000]
    
    # Benchmark non-random quicksort on:
    # a) Best-case input: Balanced partitions using generate_best_case.
    times_best = benchmark_quicksort(
        quicksort_non_random,
        lambda n: generate_best_case(list(range(n))),
        sizes
    )
    
    # b) Worst-case input: Already sorted array.
    times_worst = benchmark_quicksort(
        quicksort_non_random,
        generate_worst_case,
        sizes
    )
    
    # c) Average-case input: Random array.
    times_avg = benchmark_quicksort(
        quicksort_non_random,
        generate_average_case,
        sizes
    )
    
    # Plot the benchmark results for non-random quicksort.
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_best, label="Best Case", marker='o')
    plt.plot(sizes, times_worst, label="Worst Case", marker='o')
    plt.plot(sizes, times_avg, label="Average Case", marker='o')
    plt.xlabel("Input Size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Benchmark of Non-Random Pivot Quicksort")
    plt.legend()
    plt.grid(True)
    plt.show()
