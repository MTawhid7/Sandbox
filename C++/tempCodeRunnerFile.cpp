#include <algorithm>
#include <iostream>
#include <iterator>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>

int main() {
    std::vector<int> numbers{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Use range-based for loop
    for (const auto& number : numbers) {
        std::cout << number << " ";
    }
    std::cout << "\n";

    // Use the structured binding syntax
    auto [first, second, third] = std::tuple<int, int, int>{1, 2, 3};
    std::cout << first << " " << second << " " << third << "\n";

    // Use the std::ranges library
    std::vector<int> even_numbers;
    std::copy_if(numbers.begin(), numbers.end(), std::back_inserter(even_numbers), [](int n) { return n % 2 == 0; });
    for (const auto& number : even_numbers) {
        std::cout << number << " ";
    }
    std::cout << "\n";

    // Use string_view
    std::string_view str = "Hello, world!";
    std::cout << str << "\n";

    // Use algorithms from algorithm library with ranges
    std::vector<std::string> strings{"apple", "banana", "cherry", "durian", "elderberry"};
    std::ranges::sort(strings);
    for (const auto& s : strings) {
        std::cout << s << " ";
    }
    std::cout << "\n";

    return 0;
}
