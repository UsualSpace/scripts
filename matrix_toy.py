from fractions import Fraction
import copy

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

def checkIndex(matrix, index):
    return 0 <= index < len(matrix)

def inputMatrix():
    response = ""
    matrix = []
    while True:
        response = input("Enter row delimited by whitespace or 'stop': ")
        if response == "stop":
            break

        coefficients = response.split()
        if len(matrix) > 0 and len(coefficients) != len(matrix[0]):
            print("All rows must be the same length. Retry")
            continue
        
        for i in range(len(coefficients)):
            coefficients[i] = int(coefficients[i])

        matrix.append(coefficients)
    return matrix

def printMatrix(matrix):
    for row in matrix:
        row_str = ""
        for i in row:
            coefficient = i
            if coefficient != int(coefficient):
                coefficient = Fraction(coefficient).limit_denominator()
            row_str += f"{str(coefficient):>5} "  # right-align in width 8
        print(f"[{row_str}]")

matrix = inputMatrix()
prev_matrix = copy.deepcopy(matrix)
printMatrix(matrix)

while True:
    cmd = input(">> ")
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
        printMatrix(matrix)
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
        printMatrix(matrix)
    elif cmd[0] == "add":
        if len(cmd) != 4:
            print("Invalid add command: missing arguments.")
            continue

        target = int(cmd[1]) - 1
        source = int(cmd[2]) - 1
        scalar = eval(cmd[3])
        
        if not checkIndex(matrix, target) and not checkIndex(matrix, source):
            print("Invalid add command: indices out of range.")
            continue

        add(target, source, scalar, matrix)
        printMatrix(matrix)
    elif cmd[0] == "sub":
        if len(cmd) != 4:
            print("Invalid sub command: missing arguments.")
            continue
        
        target = int(cmd[1]) - 1
        source = int(cmd[2]) - 1
        scalar = eval(cmd[3])
        
        if not checkIndex(matrix, target) and not checkIndex(matrix, source):
            print("Invalid sub command: indices out of range.")
            continue

        sub(target, source, scalar, matrix)
        printMatrix(matrix)
    elif cmd[0] == "reset":
        matrix = inputMatrix()
        prev_matrix = copy.deepcopy(matrix)
        printMatrix(matrix)
    elif cmd[0] == "undo":
        matrix = copy.deepcopy(prev_matrix)
        printMatrix(matrix)
    elif cmd[0] == "stop":
        print("Quitting...")
        break
    else:
        print("Unknown command.")

        
        

