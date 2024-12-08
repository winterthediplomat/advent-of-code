import argparse
import re
import operator

def parse(fname):
    with open(fname) as src:
        return src.read()

def main(fname):
    text = parse(fname)

    to_search = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

    matches = re.findall(to_search, text)

    total = 0
    for each_mul in matches:
        each_mul = [int(operand) for operand in each_mul]

        total += operator.imul(*each_mul)

    print("total", total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args().fname)
