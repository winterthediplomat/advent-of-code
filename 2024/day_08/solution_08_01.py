import argparse
import re
import itertools
import pprint
import collections
import math

Position = collections.namedtuple("Position", ["x", "y"])

def parse(fname):
    result = []
    with open(fname) as src:
        for line in src:
            line = line.strip()
            result.append(list(line))
    return result

def make_equazione_retta(a: Position, b: Position):
    def eq_retta(x: int):
        delta_x = a.x - b.x
        delta_y = a.y - b.y
        return (delta_y / delta_x)*(x - a.x) + a.y
    return eq_retta

def make_equazione_retta_ruotata(a: Position, b: Position):
    def eq_retta(y: int):
        delta_x = a.y - b.y
        delta_y = a.x - b.x
        return (delta_y / delta_x)*(y - a.y) + a.x
    return eq_retta

def main(fname):
    matrix = parse(fname)

    # pprint.pprint(matrix)

    columns = len(matrix[0])

    # facciamo una mappatura di tutte le antenne
    antennas_of_freq = dict()
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == ".":
                continue
            try:
                antennas_of_freq[cell].append(Position(i, j))
            except KeyError:
                antennas_of_freq[cell] = [Position(i, j)]

    ANTINODE_ON_MAP = "#"

    set_of_unique_spots = list()

    # cerchiamo quali antenne sono sulla stessa linea, cosi' possiamo calcolare gli antinodi
    for frequency, spots in antennas_of_freq.items():
        for a_spot, b_spot in itertools.combinations(spots, 2):
            # print(a_spot, b_spot)
            # y_fun e' valida solo se le antenne non sono disposte "verticalmente"
            # nella matrice - in quel caso avremmo DivisionByZeroError, e sappiamo che bisogna gestire
            # quel caso in maniera specifica
            delta_x = a_spot.x - b_spot.x

            if delta_x != 0:
                y_fun = make_equazione_retta(a_spot, b_spot)

                first_antinode_x = a_spot.x + delta_x
                first_antinode_y = y_fun(first_antinode_x)

                second_antinode_x = a_spot.x - (2*delta_x)
                second_antinode_y = y_fun(second_antinode_x)

                is_valid_index_first = first_antinode_y.is_integer()
                is_not_out_of_bounds_first = (0 <= first_antinode_x < columns) and (0 <= first_antinode_y < columns)

                is_valid_index_second = second_antinode_y.is_integer()
                # is_not_out_of_bounds_second = (second_antinode_x < columns) and (second_antinode_y < columns)
                is_not_out_of_bounds_second = (0 <= second_antinode_x < columns) and (0 <= second_antinode_y < columns)

                if is_valid_index_first and is_not_out_of_bounds_first:
                    # matrix[first_antinode_x][int(first_antinode_y)] = ANTINODE_ON_MAP
                    set_of_unique_spots.append(Position(first_antinode_x, int(first_antinode_y)))
                if is_valid_index_second and is_not_out_of_bounds_second:
                    # matrix[second_antinode_x][int(second_antinode_y)] = ANTINODE_ON_MAP
                    set_of_unique_spots.append(Position(second_antinode_x, int(second_antinode_y)))
            else:
                x_fun = make_equazione_retta_ruotata(a_spot, b_spot)
                delta_y = a_spot.y - b_spot.y

                first_antinode_y = a_spot.y + delta_y
                first_antinode_x = x_fun(first_antinode_y)

                second_antinode_y = a_spot.y - (2*delta_y)
                second_antinode_x = x_fun(second_antinode_y)

                is_valid_index_first = first_antinode_x.is_integer()
                is_not_out_of_bounds_first = (first_antinode_y >= 0) and (first_antinode_x >= 0)

                is_valid_index_second = second_antinode_x.is_integer()
                is_not_out_of_bounds_second = (second_antinode_y < columns) and (second_antinode_x < columns)

                if is_valid_index_first and is_not_out_of_bounds_first:
                    # matrix[int(first_antinode_x)][first_antinode_y] = ANTINODE_ON_MAP
                    set_of_unique_spots.append(Position(int(first_antinode_x), first_antinode_y))
                if is_valid_index_second and is_not_out_of_bounds_second:
                    set_of_unique_spots.append(Position(int(second_antinode_x), second_antinode_y))
                    # matrix[int(second_antinode_x)][second_antinode_y] = ANTINODE_ON_MAP


    # pprint.pprint(matrix)

    total = len(set(set_of_unique_spots))
    print("total", total)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args().fname)
