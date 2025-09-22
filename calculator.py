def calculate(num1, num2, operation):
    result = 0
    
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        result = num1 / num2
    
    return result

# Test the calculator
x = 11
y = 5

addition = calculate(x, y, "add")
print(f"{x} + {y} = {addition}")

subtraction = calculate(x, y, "subtract")
print(f"{x} - {y} = {subtraction}")

multiplication = calculate(x, y, "multiply")
print(f"{x} * {y} = {multiplication}")

division = calculate(x, y, "divide")
print(f"{x} / {y} = {division}")