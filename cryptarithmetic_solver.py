import itertools
import tkinter as tk
from tkinter import messagebox

def is_valid_assignment(assignment, words, result):
    """Check if the given digit assignment satisfies the equation."""
    def word_to_number(word):
        return sum(assignment[char] * (10 ** i) for i, char in enumerate(reversed(word)))

    word_values = [word_to_number(word) for word in words]
    result_value = word_to_number(result)

    # Debugging: Print word conversions
    print(f"Trying Assignment: {assignment}")
    print(f"{' + '.join(str(w) for w in word_values)} = {result_value}")

    return sum(word_values) == result_value


def solve_cryptarithmetic(equation):
    """Solve the cryptarithmetic equation using backtracking."""
    # Extract words and result
    words_part, result = equation.split("=")
    words = words_part.replace("+", " ").split()

    # Extract unique characters
    unique_chars = sorted(set("".join(words) + result))

    if len(unique_chars) > 10:
        return None  # More than 10 unique letters, impossible to solve

    # Try all permutations of digits for unique characters
    for perm in itertools.permutations(range(10), len(unique_chars)):
        assignment = dict(zip(unique_chars, perm))

        # Ensure no word starts with zero
        if any(assignment[word[0]] == 0 for word in words + [result]):
            continue

        if is_valid_assignment(assignment, words, result):
            return assignment  # Found a valid solution

    return None  # No solution found

def on_solve():
    equation = entry.get().replace(" ", "").upper()  # Ensure uppercase letters
    solution = solve_cryptarithmetic(equation)

    if solution:
        result_str = "\n".join([f"{char} = {digit}" for char, digit in solution.items()])
        messagebox.showinfo("Solution Found", result_str)
    else:
        messagebox.showerror("No Solution", "No valid digit assignment found.")

# GUI setup
root = tk.Tk()
root.title("Cryptarithmetic Solver")
root.geometry("400x250")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Enter Cryptarithmetic Equation:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), width=20)
entry.pack(pady=5)
entry.insert(0, "SEND+MORE=MONEY")

solve_button = tk.Button(root, text="Solve", font=("Arial", 12), command=on_solve, bg="#4CAF50", fg="white")
solve_button.pack(pady=20)

root.mainloop()
