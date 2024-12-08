#!/usr/bin/env python

def parse(fname):
    left = []
    right = []
    with open(fname) as src:
        for line in src:
            line = line.strip()
            l, r = list(filter(bool, line.split(" ")))
            left.append(int(l))
            right.append(int(r))
    return (left, right)

def main(args):
    left_list, right_list = parse(args.fname)
    left_list.sort()
    right_list.sort()

    total_distance = 0
    for left, right in zip(left_list, right_list):
        total_distance += abs(left-right)

    print("total distance:", total_distance)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())
