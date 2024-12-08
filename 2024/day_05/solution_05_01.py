import argparse
import functools

def parse(fname):
    comparison_rules = dict()
    orders = []

    with open(fname) as src:
        for line in src:
            line = line.strip()
            if "|" in line:
                # is a comparison rule
                cmp_rule = list(map(int, map(str.strip, line.split("|"))))
                before, after = cmp_rule
                try:
                    comparison_rules[before][after] = -1
                except KeyError:
                    comparison_rules[before] = {after: -1}

                try:
                    comparison_rules[after][before] = 1
                except KeyError:
                    comparison_rules[after] = {before: 1}

            elif "," in line:
                new_order = list(map(int, line.split(",")))
                orders.append(new_order)

    # print(comparison_rules, orders)
    return comparison_rules, orders

def make_compare(comparison_rules):
    def fun(a, b):
        if a == b:
            return 0
        return comparison_rules[a][b]
    return fun

def middle_value(lst):
    size = len(lst)
    assert (size & 1) == 1, "size not odd!"
    middle = size >> 1
    return lst[middle]

def main(args):
    comparison_rules, orders = parse(args.fname)

    total = 0
    for order in orders:
        sorted_order = sorted(order, key=functools.cmp_to_key(make_compare(comparison_rules)))
        if order == list(sorted_order):
            to_add = middle_value(order)
            print("order", order, "is already valid! taking middle value", to_add)
            total += to_add

    print("total", total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())