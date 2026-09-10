from __future__ import annotations
import os

#Building the tokens
def tokenize(expression):

    tokens = []
    i = 0

    while i < len(expression):

        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit():

            start = i

            while i < len(expression) and expression[i].isdigit():
                i += 1

            if i < len(expression) and expression[i] == ".":

                if i + 1 >= len(expression) or not expression[i + 1].isdigit():
                    raise ValueError("Invalid number")

                i += 1

                while i < len(expression) and expression[i].isdigit():
                    i += 1

            tokens.append(("NUM", expression[start:i]))
            continue

        if char in "+-*/%^":
            tokens.append(("OP", char))
            i += 1
            continue

        if char == "(":
            tokens.append(("LPAREN", char))
            i += 1
            continue

        if char == ")":
            tokens.append(("RPAREN", char))
            i += 1
            continue

        raise ValueError("Invalid character")

    tokens.append(("END", ""))

    return tokens

#Format numbers 
def format_number(value):

    if float(value).is_integer():
        return str(int(value))

    return f"{value:.4f}".rstrip("0").rstrip(".")


def make_number_node(value):
    return ("num", float(value))


def make_unary_node(child):
    return ("neg", child)


def make_binary_node(operator, left, right):
    return ("binary", operator, left, right)

#Parse expression 
def parse_expression(tokens, position):

    left, position = parse_term(tokens, position)

    while (
        tokens[position][0] == "OP"
        and tokens[position][1] in ("+", "-")
    ):

        operator = tokens[position][1]
        position += 1

        right, position = parse_term(tokens, position)

        left = make_binary_node(
            operator,
            left,
            right
        )

    return left, position


def parse_term(tokens, position):

    left, position = parse_unary(tokens, position)

    while True:

        token_type = tokens[position][0]
        token_value = tokens[position][1]

        if token_type == "OP" and token_value in ("*", "/", "%"):

            operator = token_value
            position += 1

            right, position = parse_unary(
                tokens,
                position
            )

        elif token_type == "LPAREN":

            operator = "*"

            right, position = parse_unary(
                tokens,
                position
            )

        elif (
            token_type == "NUM"
            and position > 0
            and tokens[position - 1][0] == "RPAREN"
        ):

            operator = "*"

            right, position = parse_unary(
                tokens,
                position
            )

        else:
            break

        left = make_binary_node(
            operator,
            left,
            right
        )

    return left, position


def parse_unary(tokens, position):

    token_type = tokens[position][0]
    token_value = tokens[position][1]

    if token_type == "OP" and token_value == "-":

        child, position = parse_unary(
            tokens,
            position + 1
        )

        return make_unary_node(child), position

    if token_type == "OP" and token_value == "+":
        raise ValueError("Unary plus is not supported")

    return parse_power(tokens, position)


def parse_power(tokens, position):

    left, position = parse_primary(
        tokens,
        position
    )

    if (
        tokens[position][0] == "OP"
        and tokens[position][1] == "^"
    ):

        right, position = parse_unary(
            tokens,
            position + 1
        )

        left = make_binary_node(
            "^",
            left,
            right
        )

    return left, position


def parse_primary(tokens, position):

    token_type = tokens[position][0]
    token_value = tokens[position][1]

    if token_type == "NUM":

        return (
            make_number_node(token_value),
            position + 1
        )

    if token_type == "LPAREN":

        node, position = parse_expression(
            tokens,
            position + 1
        )

        if tokens[position][0] != "RPAREN":
            raise ValueError("Missing closing parenthesis")

        return node, position + 1

    raise ValueError("Expected a number or parenthesis")


def tree_to_string(node):

    if node[0] == "num":
        return format_number(node[1])

    if node[0] == "neg":
        return f"(neg {tree_to_string(node[1])})"

    if node[0] == "binary":

        operator = node[1]
        left = tree_to_string(node[2])
        right = tree_to_string(node[3])

        return f"({operator} {left} {right})"

    raise ValueError("Invalid tree")

#Calculate
def calculate(node):

    if node[0] == "num":
        return node[1]

    if node[0] == "neg":
        return -calculate(node[1])

    if node[0] == "binary":

        operator = node[1]

        left = calculate(node[2])
        right = calculate(node[3])

        if operator == "+":
            return left + right

        if operator == "-":
            return left - right

        if operator == "*":
            return left * right

        if operator == "/":
            return left / right

        if operator == "%":
            return left % right

        if operator == "^":
            return left ** right

    raise ValueError("Invalid expression")

#Format tokens
def format_tokens(tokens):

    output = []

    for token_type, token_value in tokens:

        if token_type == "END":
            output.append("[END]")

        else:
            output.append(
                f"[{token_type}:{token_value}]"
            )

    return " ".join(output)

#evaluation 
def evaluate_expression(expression):

    try:

        tokens = tokenize(expression)

        tree, position = parse_expression(
            tokens,
            0
        )

        if tokens[position][0] != "END":
            raise ValueError("Unexpected token")

        tree_string = tree_to_string(tree)

        token_string = format_tokens(tokens)

        try:
            value = calculate(tree)

        except Exception:
            value = "ERROR"

        return {
            "input": expression,
            "tree": tree_string,
            "tokens": token_string,
            "result": value
        }

    except Exception:

        return {
            "input": expression,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }


def evaluate_file(input_path: str) -> list[dict]:

    results = []

    with open(input_path, "r", encoding="utf-8") as file:
        expressions = file.read().splitlines()

    for expression in expressions:
        results.append(
            evaluate_expression(expression)
        )

    directory = os.path.dirname(input_path)

    if directory == "":
        directory = "."

    output_path = os.path.join(
        directory,
        "output.txt"
    )

    with open(output_path, "w", encoding="utf-8") as file:

        for index, item in enumerate(results):

            file.write(
                f"Input: {item['input']}\n"
            )

            file.write(
                f"Tree: {item['tree']}\n"
            )

            file.write(
                f"Tokens: {item['tokens']}\n"
            )

            if item["result"] == "ERROR":

                file.write(
                    "Result: ERROR\n"
                )

            else:

                file.write(
                    f"Result: {format_number(item['result'])}\n"
                )

            if index < len(results) - 1:
                file.write("\n")

    return results


if __name__ == "__main__":
    evaluate_file("input.txt")

