import argparse
import re
import operator

def parse(fname):
    with open(fname) as src:
        return src.read()

def main(fname):
    text = parse(fname)

    to_search = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))")

    matches = re.findall(to_search, text)

    total = 0
    multiplier = 1
    for each_mul in matches:
        # print(each_mul)
        if each_mul[2] == "do()":
            multiplier = 1
        elif each_mul[3] == "don't()":
            multiplier = 0
        else:
            if multiplier == 1:
                print("performable! ", each_mul)
                total += multiplier * int(each_mul[0]) * int(each_mul[1])

    print("total", total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args().fname)
