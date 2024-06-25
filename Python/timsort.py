MIN_RUN = 32

def calc_min_run(n):
    """Return the minimum length of a run from 23 - 64 so that
    the len(array)/min_run is less than or equal to a power of 2.
    """
    r = 0
    while n >= MIN_RUN:
        r |= n & 1
        n >>= 1
    return n + r

def insertion_sort(array, left, right, ascending=True):
    """Sort the array from left index to right index using insertion sort."""
    print(f"Insertion sort from index {left} to {right}, ascending={ascending}")
    for i in range(left + 1, right + 1):
        key = array[i]
        j = i - 1
        while j >= left and ((array[j] > key) if ascending else (array[j] < key)):
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    print(f"Array after insertion sort: {array[left:right+1]}")

def merge(array, left, mid, right, ascending=True):
    """Merge the sorted runs."""
    len1, len2 = mid - left + 1, right - mid
    left_part, right_part = array[left:mid + 1], array[mid + 1:right + 1]

    print(f"Merging left part {left_part} and right part {right_part}, ascending={ascending}")

    i = j = 0
    k = left

    # Use the galloping mode if one run is significantly larger
    while i < len1 and j < len2:
        if (left_part[i] <= right_part[j]) if ascending else (left_part[i] >= right_part[j]):
            array[k] = left_part[i]
            i += 1
        else:
            array[k] = right_part[j]
            j += 1
        k += 1

    while i < len1:
        array[k] = left_part[i]
        i += 1
        k += 1

    while j < len2:
        array[k] = right_part[j]
        j += 1
        k += 1

    print(f"Array after merge: {array[left:right+1]}")

def timsort(array, ascending=True):
    n = len(array)
    min_run = calc_min_run(n)

    print(f"Calculated minimum run size: {min_run}")

    # Sort individual subarrays of size RUN
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(array, start, end, ascending)

    # Start merging from size RUN (or min_run). It will merge
    # to form size 64, 128, 256 and so on ....
    size = min_run
    while size < n:
        for left in range(0, n, size * 2):
            mid = min(n - 1, left + size - 1)
            right = min((left + size * 2 - 1), (n - 1))

            # Merge subarray array[left...mid] & array[mid+1...right]
            if mid < right:
                merge(array, left, mid, right, ascending)
        size *= 2

# Example usage:
if __name__ == "__main__":
    # Input the array from the user
    user_input = input("Enter the elements of the array, separated by spaces: ")
    array = list(map(float, user_input.split()))

    order = input("Do you want to sort the array in increasing or decreasing order? (i/d): ").strip().lower()
    ascending = order == 'i'

    print("Original array:")
    print(array)

    timsort(array, ascending)

    print("Sorted array:")
    print(array)
