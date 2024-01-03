#include <iostream>
#include <vector>

// Merge two subarrays of arr[]
// First subarray is arr[left..middle]
// Second subarray is arr[middle+1..right]
void merge(std::vector<int>& arr, int left, int middle, int right) {
    int n1 = middle - left + 1;
    int n2 = right - middle;

    // Create temporary arrays
    std::vector<int> LeftArray(n1);
    std::vector<int> RightArray(n2);

    // Copy data to temporary arrays LeftArray[] and RightArray[]
    for (int i = 0; i < n1; ++i)
        LeftArray[i] = arr[left + i];
    for (int j = 0; j < n2; ++j)
        RightArray[j] = arr[middle + 1 + j];

    // Merge the temporary arrays back into arr[left..right]
    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (LeftArray[i] <= RightArray[j]) {
            arr[k] = LeftArray[i];
            i++;
        } else {
            arr[k] = RightArray[j];
            j++;
        }
        k++;
    }

    // Copy the remaining elements of LeftArray[], if any
    while (i < n1) {
        arr[k] = LeftArray[i];
        i++;
        k++;
    }

    // Copy the remaining elements of RightArray[], if any
    while (j < n2) {
        arr[k] = RightArray[j];
        j++;
        k++;
    }
}

// Main function to sort an array using merge sort algorithm
void mergeSort(std::vector<int>& arr, int left, int right) {
    if (left < right) {
        // Find the middle point to divide the array into two halves
        int middle = left + (right - left) / 2;

        // Recursively sort the first and second halves
        mergeSort(arr, left, middle);
        mergeSort(arr, middle + 1, right);

        // Merge the sorted halves
        merge(arr, left, middle, right);
    }
}

// Function to print an array
void printArray(const std::vector<int>& arr) {
    for (int num : arr) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
}

int main() {
    std::vector<int> arr;
    int element;
    std::cout << "Enter the elements of the array separated by spaces (enter a non-integer character to stop): ";

    // Take user input for array elements
    while (std::cin >> element) {
        arr.push_back(element);
    }

    std::cout << "Given array is \n";
    printArray(arr);

    mergeSort(arr, 0, arr.size() - 1);

    std::cout << "Sorted array is \n";
    printArray(arr);

    return 0;
}
