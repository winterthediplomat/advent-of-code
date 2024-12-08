import argparse
import re
import itertools
import pprint

def parse(fname):
    result = []
    with open(fname) as src:
        for line in src:
            line = line.strip()
            result.append(list(line))
    return result


X_COORDINATES = lambda i, j: [(i-1, j-1), (i, j), (i+1, j+1), (i-1, j+1), (i, j), (i+1, j-1)]

def template2(i, j, matrix, coordinates):
    try:
        values = [matrix[a][b] for a, b in coordinates(i, j) if a >=0 and b >= 0]
        return "".join(values[:3]) in ["MAS", "SAM"] and "".join(values[3:]) in ["MAS", "SAM"]
    except IndexError:
        return False

def main(fname):
    matrix = parse(fname)

    rows = len(matrix)
    columns = len(matrix[0]) # assumiamo siano tutte uguali

    total = 0
    to_keep = []
    for i, j in itertools.product(range(rows), range(columns)):
        check_functions = [
                (lambda i, j, matrix: template2(i, j, matrix, X_COORDINATES) , "X", X_COORDINATES),

        ]
    
        for check_fun, direction, coordfun in check_functions:
            if check_fun(i, j, matrix):
                print("XMAS starting from {},{} and going {}".format(i, j, direction))
                to_keep.append(((i, j), coordfun))
                total += 1


    new_matrix = [["." for i in range(columns)] for j in range(rows)]
    for (i, j), coordfun in to_keep:
        for c_i, c_j in coordfun(i, j):
            new_matrix[c_i][c_j] = matrix[c_i][c_j]

    for idx, row in enumerate(new_matrix):
        new_matrix[idx] = "".join(row)

    pprint.pprint(new_matrix)

    print("total", total)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args().fname)
