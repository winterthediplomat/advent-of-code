import argparse
import functools

def parse(fname):
    with open(fname) as src:
        line = src.read()
        line = line.strip()

    for stone in line.split(" "):
        yield int(stone)

@functools.cache
def evolve(stone, times):
    if times == 0:
        return 1
    
    # rule 1 
    if stone == 0:
        return evolve(1, times-1)
    # rule 2
    as_str = str(stone)
    if len(as_str) % 2 == 0:
        half_size = len(as_str) // 2
        left_num, right_num = int(as_str[:half_size]), int(as_str[half_size:])
        return evolve(left_num, times-1) + evolve(right_num, times-1)
    # rule 3
    return evolve(stone*2024, times-1)

def main(args):
    stones = parse(args.fname)

    total_25 = 0
    total_75 = 0
    for stone in stones:
        total_25 += evolve(stone, 25)
        total_75 += evolve(stone, 75)

    print("total (25 blinks)", total_25)
    print("total (75 blinks)", total_75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())
