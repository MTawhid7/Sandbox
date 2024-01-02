import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class App {
    public static void main(String[] args) {
        // Java 9 - Collection factory methods
        List<String> colors = List.of("Red", "Green", "Blue", "Yellow");

        // Java 10 - Local variable type inference (var)
        var mixedColors = Stream.of("Purple", "Orange").collect(Collectors.toList());

        // Java 11 - String methods (isBlank, lines, repeat)
        var text = "   Hello, World!   ";
        System.out.println("Text is blank: " + text.isBlank());
        var lines = text.lines().collect(Collectors.toList());
        System.out.println("Lines: " + lines);
        var repeatedText = text.repeat(3);
        System.out.println("Repeated text: " + repeatedText);

        // Java 12 - Teeing Collector
        var combinedColors = Stream.concat(colors.stream(), mixedColors.stream())
                                   .collect(Collectors.teeing(
                                           Collectors.toSet(),
                                           Collectors.toUnmodifiableList(),
                                           (set, list) -> "Distinct colors: " + set + ", All colors: " + list
                                   ));
        System.out.println(combinedColors);

        // Java 14 - Switch expressions (enhanced switch)
        int month = 8;
        String monthString = switch (month) {
            case 1 -> "January";
            case 2 -> "February";
            // ... cases for other months
            default -> "Unknown month";
        };
        System.out.println("Month: " + monthString);

        // Java 16 - Text Blocks
        var poem = """
            Roses are red,
            Violets are blue,
            This code uses text blocks,
            And so can you!
            """;
        System.out.println(poem);

        // Java 17 - Record Classes (immutable classes)
        record Person(String name, int age) {
        }

        Person person1 = new Person("Alice", 30);
        Person person2 = new Person("Alice", 30); // Different object, but equal
        System.out.println(person1.equals(person2)); // Output: true

        // Java 19 - Virtual Threads (example using standard threads)
        Thread thread = new Thread(() -> System.out.println("Running on a standard thread"));
        thread.start();
    }
}
