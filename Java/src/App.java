import java.util.ArrayList;
import java.util.Scanner;

public class App {
    // Merge two subarrays of arr[]
    // First subarray is arr[left..middle]
    // Second subarray is arr[middle+1..right]
    public static void merge(ArrayList<Integer> arr, int left, int middle, int right) {
        int n1 = middle - left + 1;
        int n2 = right - middle;

        // Create temporary arrays
        ArrayList<Integer> LeftArray = new ArrayList<>(n1);
        ArrayList<Integer> RightArray = new ArrayList<>(n2);

        // Copy data to temporary arrays LeftArray[] and RightArray[]
        for (int i = 0; i < n1; ++i)
            LeftArray.add(arr.get(left + i));
        for (int j = 0; j < n2; ++j)
            RightArray.add(arr.get(middle + 1 + j));

        // Merge the temporary arrays back into arr[left..right]
        int i = 0, j = 0, k = left;
        while (i < n1 && j < n2) {
            if (LeftArray.get(i) <= RightArray.get(j)) {
                arr.set(k, LeftArray.get(i));
                i++;
            } else {
                arr.set(k, RightArray.get(j));
                j++;
            }
            k++;
        }

        // Copy the remaining elements of LeftArray[], if any
        while (i < n1) {
            arr.set(k, LeftArray.get(i));
            i++;
            k++;
        }

        // Copy the remaining elements of RightArray[], if any
        while (j < n2) {
            arr.set(k, RightArray.get(j));
            j++;
            k++;
        }
    }

    // Main function to sort an array using merge sort algorithm
    public static void mergeSort(ArrayList<Integer> arr, int left, int right) {
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
    public static void printArray(ArrayList<Integer> arr) {
        for (int num : arr) {
            System.out.print(num + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ArrayList<Integer> arr = new ArrayList<>();
        System.out
                .print("Enter the elements of the array separated by spaces (enter a non-integer character to stop): ");

        // Take user input for array elements
        while (scanner.hasNextInt()) {
            arr.add(scanner.nextInt());
        }

        System.out.println("Given array is:");
        printArray(arr);

        mergeSort(arr, 0, arr.size() - 1);

        System.out.println("Sorted array is:");
        printArray(arr);

        scanner.close();
    }
}
