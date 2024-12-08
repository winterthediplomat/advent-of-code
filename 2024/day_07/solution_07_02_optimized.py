import argparse
import collections
#from types import List
import functools
import operator
import pprint
import math

Line = collections.namedtuple("Line", ["total", "operands"])

def parse(fname):
    result = []
    with open(fname) as src:
        for line in src:
            line = line.strip()
            total, operands = line.split(":")
            total = int(total.strip())
            operands = list(map(int, filter(bool, operands.split(" "))))

            result.append(Line(total, operands))
    return result

def evaluate(line: Line, operators):
    a, b = line.operands[:2]
    for op in operators:
        intermediate_result = op(a, b)
        if intermediate_result < line.total:
            if len(line.operands) == 2:
                # no operators slots remaining, the situation
                # cannot get better - do not call evaluate with just one operand
                continue

            # we still have room for some other operations
            intermediate_line = Line(line.total, [intermediate_result] + line.operands[2:])
            following_operators = evaluate(intermediate_line, operators)
            if following_operators:
                # subsequent calculations managed to arrive to the total! yay!
                return [op] + following_operators
            else:
                # skip - the choice of this operator did not help create a correct equation
                continue
        elif intermediate_result > line.total:
            # skip - we overshoot, so it's no use to continue
            continue
        elif intermediate_result == line.total:
            if len(line.operands) > 2:
                intermediate_line = Line(line.total, [intermediate_result] + line.operands[2:])
                following_operators = evaluate(intermediate_line, operators)
                if following_operators:
                    # other operands cannot change the verdict: we found a possible way to get the total!
                    return [op] + following_operators
                else:
                    # other operands will ruin it :(
                    continue 
            elif len(line.operands) == 2:
                # good case!
                return [op]
    else:
        # we reach this part if no good cases have been found
        return None 

def concatenate(a, b):
    # small constant added to avoid special-casing other=1, 10, 100, ...
    shift = math.ceil(math.log10(b+0.0000001))
    return (a * 10**shift) + b 
    # return int(str(a) + str(b))
    

OPERATORS = [
    (operator.add, "+"),
    (operator.mul, "*"),
    (concatenate, "||")
]

def main(args):
    lines: List[Line] = parse(args.fname)

    sum_of_obtainables = 0
    for line in lines:

        list_of_operators = evaluate(line, [op for op, _ in OPERATORS])
        can_be_obtainable = bool(list_of_operators)
        if can_be_obtainable:
            # print(line , "-->", list_of_operators)
            sum_of_obtainables += line.total
        else:
            pass # print("wrong expression", line)
    print("total", sum_of_obtainables)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())
