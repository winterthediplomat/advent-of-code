#!/usr/bin/env bash

import argparse

def parse(fname):
    result = []
    with open(fname) as src:
        for line in src:
            line = line.strip()
            result.append(list(map(lambda c: int(c) if c in "0123456789" else c, line)))
    return result


up = lambda coords: (coords[0]-1, coords[1])
down = lambda coords: (coords[0]+1, coords[1]) 
left = lambda coords: (coords[0], coords[1]-1) 
right = lambda coords: (coords[0], coords[1]+1)

def are_valid_coords(topomap, coords, value_moved_from):
    try:
        assert coords[0] >= 0
        assert coords[0] < len(topomap)
        assert coords[1] >= 0
        assert coords[1] < len(topomap[0])
        assert 1 == (topomap[coords[0]][coords[1]] - value_moved_from)
        return True, coords
    except AssertionError:
        return False, coords
    except TypeError:
        # per poter provare gli esempi
        return False, coords


def visit(topomap, current_coords, reachable_summits=None):
    current_value = topomap[current_coords[0]][current_coords[1]]
    
    if current_value == 9:
        # print("found something!", current_coords)
        reachable_summits.append(current_coords) 
        return True

    ok, coords = are_valid_coords(topomap, up(current_coords), current_value)
    if ok:
        visit(topomap, coords, reachable_summits)

    ok, coords = are_valid_coords(topomap, down(current_coords), current_value)
    if ok:
        visit(topomap, coords, reachable_summits)

    ok, coords = are_valid_coords(topomap, left(current_coords), current_value)
    if ok:
        visit(topomap, coords, reachable_summits)

    ok, coords = are_valid_coords(topomap, right(current_coords), current_value)
    if ok:
        visit(topomap, coords, reachable_summits)

def main(args):
    learscail = parse(args.fname)

    visited_ends = []
    total = 0
    for i, row in enumerate(learscail):
        for j, point in enumerate(row):
            if point == 0:
                ends_from_here = [] 
                visit(learscail, (i, j), ends_from_here)
                total += len(ends_from_here)
                visited_ends.extend(ends_from_here)

    print("total ratings", len(visited_ends))
    print("total scores", total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())
