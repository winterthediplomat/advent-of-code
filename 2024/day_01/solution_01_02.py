#!/usr/bin/env python
import collections

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

    left_set = set(left_list)
    right_counter = collections.Counter(right_list)

    total = 0
    for left_item in left_set:
        total += left_item * right_counter[left_item]

    print("total: ", total)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())
