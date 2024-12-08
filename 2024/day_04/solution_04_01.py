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


FULL_RIGHT_COORDINATES = lambda i, j: [(i, j), (i, j+1), (i, j+2), (i, j+3)]
FULL_LEFT_COORDINATES = lambda i, j: [(i, j), (i, j-1), (i, j-2), (i, j-3)]
FULL_UP_COORDINATES = lambda i, j: [(i, j), (i-1, j), (i-2, j), (i-3, j)]
FULL_DOWN_COORDINATES = lambda i, j: [(i, j), (i+1, j), (i+2, j), (i+3, j)]
NORTHWEST_COORDINATES = lambda i, j: [(i, j), (i-1, j-1), (i-2, j-2), (i-3, j-3)]
NORTHEAST_COORDINATES = lambda i, j: [(i, j), (i-1, j+1), (i-2, j+2), (i-3, j+3)]
SOUTHWEST_COORDINATES = lambda i, j: [(i, j), (i+1, j-1), (i+2, j-2), (i+3, j-3)]
SOUTHEAST_COORDINATES = lambda i, j: [(i, j), (i+1, j+1), (i+2, j+2), (i+3, j+3)]

def template(i, j, matrix, coordinates):
    try:
        values = [matrix[a][b] for a, b in coordinates(i, j) if a >=0 and b >= 0]
        return values == ["X", "M", "A", "S"]
    except IndexError:
        return False

def check_full_right(i, j, matrix):
    return template(i, j, matrix, FULL_RIGHT_COORDINATES)

def check_full_left(i, j, matrix):
    return template(i, j, matrix, FULL_LEFT_COORDINATES)

def check_full_up(i, j, matrix):
    return template(i, j, matrix, FULL_UP_COORDINATES)

def check_full_down(i, j, matrix):
    return template(i, j, matrix, FULL_DOWN_COORDINATES)

def check_northwest(i, j, matrix):
    return template(i, j, matrix, NORTHWEST_COORDINATES)

def check_northeast(i, j, matrix):
    return template(i, j, matrix, NORTHEAST_COORDINATES)

def check_southeast(i, j, matrix):
    return template(i, j, matrix, SOUTHEAST_COORDINATES)

def check_southwest(i, j, matrix):
    return template(i, j, matrix, SOUTHWEST_COORDINATES)

def main(fname):
    matrix = parse(fname)

    rows = len(matrix)
    columns = len(matrix[0]) # assumiamo siano tutte uguali

    total = 0
    to_keep = []
    for i, j in itertools.product(range(rows), range(columns)):
        check_functions = [
                (check_full_left, "full left", FULL_LEFT_COORDINATES),
                (check_full_right, "full right", FULL_RIGHT_COORDINATES),
                (check_full_up, "full up", FULL_UP_COORDINATES),
                (check_full_down, "full down", FULL_DOWN_COORDINATES),
                (check_northeast, "northeast", NORTHEAST_COORDINATES),
                (check_northwest, "northwest", NORTHWEST_COORDINATES),
                (check_southeast, "southeast", SOUTHEAST_COORDINATES),
                 (check_southwest, "southwest", SOUTHWEST_COORDINATES)
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
