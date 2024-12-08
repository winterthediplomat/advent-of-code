import argparse

from collections import Counter

def parse(fname):
    result = []

    with open(fname) as src:
        for line in src:
            line = line.strip()
            numbers = list(map(int, line.split(" ")))
            result.append(numbers)

    return result


def main(args):
    levels = parse(args.fname)

    safe = 0
    dampened = 0
    for level in levels:
        all_ascending = all(a < b for a, b in zip(level[:-1], level[1:]))
        all_descending = all(a > b for a, b in zip(level[:-1], level[1:]))
        distance_counter = [1 <= abs(a-b) <= 3 for (a, b) in zip(level[:-1], level[1:])]
        distance_respected = all(check for check in distance_counter)
    
        if (all_ascending or all_descending) and distance_respected:
            print(level, "--> safe")
            safe += 1
        else:
            # apply problem dampener!
            print("level", level)

            for pos in range(len(level)):
                checkable = [value for value, _ in filter(lambda it: it[1] != pos, ((value, idx) for idx, value in enumerate(level)))]
                print("check #{}: {}".format(pos, checkable))
                all_ascending = all(a < b for a, b in zip(checkable[:-1], checkable[1:]))
                all_descending = all(a > b for a, b in zip(checkable[:-1], checkable[1:]))
                distance_counter = [1 <= abs(a-b) <= 3 for (a, b) in zip(checkable[:-1], checkable[1:])]
                distance_respected = all(check for check in distance_counter)

                if (all_ascending or all_descending) and distance_respected:
                    print("--> dampened")
                    safe += 1
                    dampened += 1
                    break # skip checking this level, we found a solution

    print("safe reports", safe, "of which ", dampened, "are dampened")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())
