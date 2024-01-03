def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

    return arr


# Get input from the user
print("Enter elements to sort (space-separated):")
user_input = input().split()

my_array = [int(num) for num in user_input]

sorted_array = insertion_sort(my_array)
print("Sorted array:", sorted_array)
