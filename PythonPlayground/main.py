import typing
import asyncio

# Type hints for clarity and static type checkers
def get_user_info(name: str, age: int) -> typing.Tuple[str, int]:
    return name.title(), age * 2  # Chained operations for conciseness

# Exception groups for handling multiple exceptions gracefully
try:
    # Code that might raise multiple exceptions
    print(get_user_info("Alice", 30))
except (ValueError, TypeError) as e:
    print("Invalid input encountered:", e)

# Task groups for cooperative multitasking (preview feature)
async def task1():
    await asyncio.sleep(1)
    print("Task 1 completed")

async def task2():
    await asyncio.sleep(2)
    print("Task 2 completed")

async def main():
    await asyncio.gather(task1(), task2())  # Run tasks concurrently

# Structural pattern matching for flexible data extraction
data = {"name": "Alice", "age": 30}
match data:
    case {"name": name, "age": age}:
        formatted_string = f"Hello, {name}"  # Define `name` within the indented block
        print(formatted_string)
        print(f"Name: {name}, Age: {age}")
    case _:
        print("Unexpected data format")

# Enhanced dictionary merging for cleaner updates
updated_data = {**data, "city": "New York"}  # Merge dictionaries concisely

# To run this code, make sure you have Python 3.12 or later installed.
