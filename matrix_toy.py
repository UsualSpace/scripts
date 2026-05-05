from fractions import Fraction
import copy

#TODO: better handling of fractions, decimals, eval.
#TODO: Rewrite set command to be consistent with other commands.
#TODO: Allow toggle between fraction and decimal coefficient representations
#TODO: provide a command rewind feature.

def swap(a, b, matrix):
    for i in range(len(matrix[a])):
        temp = matrix[a][i]
        matrix[a][i] = matrix[b][i]
        matrix[b][i] = temp

def mul(target, scalar, matrix):
    for i in range(len(matrix[target])):
        matrix[target][i] = matrix[target][i] * scalar

def add(target, source, scalar, matrix):
    for i in range(len(matrix[target])):
        matrix[target][i] = matrix[target][i] + matrix[source][i] * scalar

def sub(target, source, scalar, matrix):
    for i in range(len(matrix[target])):
        matrix[target][i] = matrix[target][i] - matrix[source][i] * scalar

def rref(matrix):
    row = 0
    for i in range(len(matrix[0]) - 1):
        if matrix[row][i] != 1 and matrix[row][i] != 0:
            mul(row, 1.0 / matrix[row][i], matrix)
        for j in range(len(matrix)):
            if j == row: continue
            if matrix[j][i] != 0:
                sub(j, row, matrix[j][i], matrix)
        row += 1

# def myEval(expression):
#     #Perform lexical analysis - extract tokens
#     tokens = [("begin")]
#     group = ""
#     special = "()+-*/"
#     precedence = {"add": 1, "sub": 1, "mul": 2, "div": 2, "neg": 3}
#     associativity = {"add": 0, "sub": 0, "mul": 0, "div": 0, "neg": 1}
#     #TODO: There has to be a more elegant way to do this.
#     for c in expression:
#         if c == " ":
#             continue
#         if c not in special:
#             group += c
#         else:
#             if len(group) > 0:
#                 tokens.append(("number", group))
#                 group = ""
#             if c == "(":
#                 tokens.append(("lparen", "("))
#             elif c == ")":
#                 tokens.append(("rparen", ")"))
#             elif c == "+":
#                 tokens.append(("binop", "+", precedence["add"], associativity["add"]))
#             elif c == "-":
#                 last_token = tokens[-1]
#                 if last_token[0] == "begin" or last_token[0] == "binop" or last_token[0] == "lparen":
#                     tokens.append(("unop", "-", precedence["neg"], associativity["neg"]))
#                 else:
#                     tokens.append(("binop", "-", precedence["sub"], associativity["sub"]))
#             elif c == "*":
#                 tokens.append(("binop", "*", precedence["mul"], associativity["mul"]))
#             elif c == "/":
#                 tokens.append(("binop", "/", precedence["div"], associativity["div"]))
#     if len(group) > 0: tokens.append(("number", group))

#     print(tokens)

#     #Convert to post fix notation TODO: error handle
#     post_fix_tokens = []
#     operators = []
#     for token in tokens:
#         if token[0] == "number":
#             post_fix_tokens.append(token)
#         elif token[0] == "binop" or token[0] == "unop":
#             while len(operators) > 0 and operators[-1][0] != "lparen" and (operators[-1][2] >= token[2]):
#                 #or (operators[-1][2] == token[2] and token[3] == 0) TODO: Investigate why this extra condition makes it incorrect
#                 post_fix_tokens.append(operators.pop())
#             operators.append(token)
#         elif token[0] == "(":
#             operators.append(token)
#         elif token[0] == ")":
#             #TODO: handle mismatched parentheses.
#             while len(operators) > 0 and operators[-1][0] != "(":
#                 post_fix_tokens.append(operators.pop())
#             operators.pop()
#     while len(operators) > 0:
#         post_fix_tokens.append(operators.pop())

#     print(post_fix_tokens)
#     try:
#         #Evaluate expression using stack
#         operands = []
#         for token in post_fix_tokens:
#             if token[0] == "number":
#                 operands.append(float(token[1]))
#             elif token[1] == "+":
#                 rhs = operands.pop()
#                 lhs = operands.pop()
#                 operands.append(lhs + rhs)
#             elif token[1] == "-":
#                 rhs = operands.pop()
#                 if token[0] == "unop":
#                     operators.append(rhs * -1)
#                     continue
#                 lhs = operands.pop()
#                 operands.append(lhs - rhs)
#             elif token[1] == "*":
#                 rhs = operands.pop()
#                 lhs = operands.pop()
#                 operands.append(lhs * rhs)
#             elif token[1] == "/":
#                 rhs = operands.pop()
#                 lhs = operands.pop()
#                 operands.append(lhs / rhs)
#         return operands[0]
#     except (ValueError, TypeError) as e:
#         print(e)
#         print("Invalid expression.")
#         return 

def checkIndex(matrix, index):
    return 0 <= index < len(matrix)

def setMatrix():
    response = ""
    matrix = []
    print("================== MATRIX BUILDER ==================")
    while True:
        response = input("Enter a row delimited by whitespace or 'stop': ")
        if response == "stop":
            break

        coefficients = response.split()
        if len(matrix) > 0 and len(coefficients) != len(matrix[0]):
            print("All rows must be the same length. Retry")
            continue
        
        try:
            for i in range(len(coefficients)):
                coefficients[i] = float(coefficients[i])
        except (ValueError, TypeError):
            print("Rows must only contain numbers. Retry")
            continue

        matrix.append(coefficients)
    return matrix

def printMatrix(matrix):
    for row in matrix:
        row_str = ""
        for i in row:
            coefficient = i
            if isinstance(coefficient, float):
                coefficient = Fraction(coefficient).limit_denominator()
                if coefficient.denominator == 1:
                    coefficient = coefficient.numerator
            row_str += f"{str(coefficient):>5} "  # right-align in width 8
        print(f"[{row_str}]")

cmds = [
    "add (ex: add [target row idx 1..n] [source row idx 1..n] [scalar multiplier for source row])",
    "sub (ex: sub [target row idx 1..n] [source row idx 1..n] [scalar multiplier for source row])",
    "mul (ex: mul [target row idx 1..n] [scalar multiplier for source row])",
    "swap (ex: swap [row a idx 1..n] [row b idx 1..n])",
    "undo",
    "redo",
    "set",
    "undoall",
    "redoall",
    "help",
    "stop",
    "v++",
    "v--",
    "rref",
    "load",
    "store"
]

MAX_VERBOSITY = 2

verbosity_level = 0
stop = False
matrix = setMatrix()
printMatrix(matrix)
matrix_history = []
matrices = {}

while True:
    commands = input(">> ")
    commands = commands.split("|") # For a command sequence to be executed from left to right
    mutated = False
    for cmd in commands:
        cmd = cmd.split()
        if cmd[0] == "swap":
            if len(cmd) != 3:
                print("Invalid swap command: missing arguments.")
                continue

            a = int(cmd[1]) - 1
            b = int(cmd[2]) - 1
            
            if not checkIndex(matrix, a) and not checkIndex(matrix, b):
                print("Invalid mul command: index out of range.")
                continue

            swap(a, b, matrix)
            mutated = True
            
            if verbosity_level == 1: print(f"Swapped row {a} and row {b}")
            if verbosity_level == 2: printMatrix(matrix) 
        elif cmd[0] == "mul":
            if len(cmd) != 3:
                print("Invalid mul command: missing arguments.")
                continue

            target = int(cmd[1]) - 1
            scalar = eval(cmd[2])
            
            if not checkIndex(matrix, target):
                print("Invalid mul command: index out of range.")
                continue

            mul(target, scalar, matrix)
            mutated = True

            if verbosity_level == 1: print(f"Multiplying row {a} by {cmd[2]})")
            if verbosity_level == 2: printMatrix(matrix) 
        elif cmd[0] == "add":
            if len(cmd) < 3:
                print("Invalid add command: missing arguments.")
                continue
            
            target = int(cmd[1]) - 1
            source = int(cmd[2]) - 1
            scalar = 1
            #If a 4th argument is present, interpret it as a scalar multiple to apply to the operation.
            if len(cmd) == 4:
                scalar = eval(cmd[3])
            
            if not checkIndex(matrix, target) and not checkIndex(matrix, source):
                print("Invalid add command: indices out of range.")
                continue

            add(target, source, scalar, matrix)
            mutated = True

            if verbosity_level == 1: print(f"Added {cmd[3]} * row {source} to row {target}")
            if verbosity_level == 2: printMatrix(matrix)
        elif cmd[0] == "sub":
            if len(cmd) < 3:
                print("Invalid sub command: missing arguments.")
                continue
            
            target = int(cmd[1]) - 1
            source = int(cmd[2]) - 1
            scalar = 1
            #If a 4th argument is present, interpret it as a scalar multiple to apply to the operation.
            if len(cmd) == 4:
                scalar = eval(cmd[3])
            
            if not checkIndex(matrix, target) and not checkIndex(matrix, source):
                print("Invalid sub command: indices out of range.")
                continue

            sub(target, source, scalar, matrix)
            mutated = True

            if verbosity_level == 1: print(f"Subtracted {cmd[3]} * row {source} from row {target}")
            if verbosity_level == 2: printMatrix(matrix)
        elif cmd[0] == "undo":
            if matrix_idx - 1 < 0:
                print("Nothing to undo.")
            else:
                matrix_idx -= 1
                matrix = copy.deepcopy(matrix_history[matrix_idx])
                if verbosity_level == 1: print("Undid operation")
        elif cmd[0] == "redo":
            if matrix_idx + 1 > len(matrix_history) - 1:
                print("Nothing to redo.")
            else:
                matrix_idx += 1
                matrix = copy.deepcopy(matrix_history[matrix_idx])
                if verbosity_level == 1: print("Redid operation")
        elif cmd[0] == "set":
            matrix = setMatrix()
            mutated = True
        elif cmd[0] == "undoall":
            matrix_idx = 0
            matrix = copy.deepcopy(matrix_history[matrix_idx])
            if verbosity_level == 1: print("Undid all previous operations.")
        elif cmd[0] == "redoall":
            matrix_idx = len(matrix_history) - 1
            matrix = copy.deepcopy(matrix_history[matrix_idx])
            if verbosity_level == 1: print("Redid all future operations.")
        elif cmd[0] == "stop":
            print("Stopping...")
            stop = True 
            break
        elif cmd[0] == "help":
            print("Available commands:")
            for cmd_name in cmds:
                print(cmd_name)
            continue
        elif cmd[0] == "v++":
            verbosity_level = min(MAX_VERBOSITY, verbosity_level + 1)
            continue
        elif cmd[0] == "v--":
            verbosity_level = max(0, verbosity_level - 1)
            continue
        elif cmd[0] == "rref":
            rref(matrix)
            mutated = True
        else:
            print("Unknown command.")
            continue

    if mutated:
        if len(matrix_history) > 1 and matrix_idx != len(matrix_history) - 1:
            for i in range(len(matrix_history) - 1, matrix_idx, -1):
                matrix_history.pop()
        
        matrix_history.append(copy.deepcopy(matrix))
        matrix_idx = len(matrix_history) - 1

    if stop: break
    printMatrix(matrix)
        
        

