import argparse

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
    for level in levels:
        all_ascending = all(a < b for a, b in zip(level[:-1], level[1:]))
        all_descending = all(a > b for a, b in zip(level[:-1], level[1:]))
        distance_respected = all(1 <= abs(a-b) <= 3 for a, b in zip(level[:-1], level[1:]))
    

        if (all_ascending or all_descending) and distance_respected:
            safe += 1
        else:
            pass # print("not safe! ascending? {} descending? {} distance respected? {}".format(all_ascending, all_descending, distance_respected))

    print("safe reports", safe)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())
