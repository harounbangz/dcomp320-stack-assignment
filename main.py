class Stack:
    """Standard LIFO Stack data structure using Python list."""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Pop requested from an empty stack.")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


def precedence(op):
    """Returns operator precedence rank."""
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

def apply_op(op, b, a):
    """Applies arithmetic operator to two numbers."""
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        return a / b
    return 0

def tokenize(expression):
    """Splits string into numbers, operators, and parentheses."""
    tokens = []
    i = 0
    n = len(expression)
    while i < n:
        char = expression[i]
        if char.isspace():
            i += 1
            continue
        if char.isdigit() or char == '.':
            num_str = ""
            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                num_str += expression[i]
                i += 1
            tokens.append(float(num_str) if '.' in num_str else int(num_str))
            continue
        if char in "+-*/()":
            tokens.append(char)
        i += 1
    return tokens



def evaluate_expression(expression):
    """
    Evaluates infix expression using dual-stack logic.
    Handles +, -, *, /, precedence, and parentheses.
    """
    tokens = tokenize(expression)
    values = Stack()
    ops = Stack()

    for token in tokens:
        if isinstance(token, (int, float)):
            values.push(token)
        elif token == '(':
            ops.push(token)
        elif token == ')':
            while not ops.is_empty() and ops.peek() != '(':
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.push(apply_op(op, val2, val1))
            ops.pop()  # Remove '('
        elif token in "+-*/":
            while (not ops.is_empty() and 
                   precedence(ops.peek()) >= precedence(token)):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()
                values.push(apply_op(op, val2, val1))
            ops.push(token)

    while not ops.is_empty():
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()
        values.push(apply_op(op, val2, val1))

    result = values.pop()
    return int(result) if isinstance(result, float) and result.is_integer() else result



import os

def process_file(input_filename="input.txt", output_filename="output.txt"):
    """Reads input.txt, evaluates multi-line expressions, and writes to output.txt."""
    if not os.path.exists(input_filename):
        print(f"Error: {input_filename} not found.")
        return

    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    output_lines = []
    current_expr = []

    for line in lines:
        stripped = line.strip()
        if stripped == "-----":
            if current_expr:
                full_expr = " ".join(current_expr)
                res = evaluate_expression(full_expr)
                output_lines.append(f"{res}\n")
                current_expr = []
            output_lines.append("-----\n")
        elif stripped:
            current_expr.append(stripped)

    if current_expr:
        full_expr = " ".join(current_expr)
        res = evaluate_expression(full_expr)
        output_lines.append(f"{res}\n")

    with open(output_filename, 'w') as outfile:
        outfile.writelines(output_lines)

    print(f"Processing complete. Output saved to {output_filename}")

if __name__ == "__main__":
    process_file()