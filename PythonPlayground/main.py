def generate_fibonacci(limit):
    fibonacci_sequence = []
    a, b = 0, 1
    while a < limit:
        fibonacci_sequence.append(a)
        a, b = b, a + b
    return fibonacci_sequence


# Generating Fibonacci sequence up to a limit of 100
limit = 100
fib_sequence = generate_fibonacci(limit)

print(f"Fibonacci sequence up to {limit}:")
print(fib_sequence)
