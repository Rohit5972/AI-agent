# tests.py

from functions.run_python_file import run_python_file

# Test 1: Run main.py without arguments (should print usage instructions)
result1 = run_python_file("calculator", "main.py")
print("Test 1 result:\n", result1, "\n")

# Test 2: Run main.py with a calculation argument (should evaluate expression)
result2 = run_python_file("calculator", "main.py", ["3 + 5"])
print("Test 2 result:\n", result2, "\n")

# Test 3: Run tests.py itself (may produce output depending on its contents)
result3 = run_python_file("calculator", "tests.py")
print("Test 3 result:\n", result3, "\n")

# Test 4: Attempt to run a file outside the working directory (should return error)
result4 = run_python_file("calculator", "../main.py")
print("Test 4 result:\n", result4, "\n")

# Test 5: Attempt to run a non-existent file (should return error)
result5 = run_python_file("calculator", "nonexistent.py")
print("Test 5 result:\n", result5, "\n")
