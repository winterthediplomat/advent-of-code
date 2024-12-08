import argparse
import collections
#from types import List
import functools
import operator
import pprint

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

# def evaluate(line: Line, operators, indent=0):
def evaluate(line: Line, operators):
    if len(line.operands) == 1:
        if line.operands[0] == line.total:
            return ["identity"] 
        else:
            return None

    a, b = line.operands[:2]
    for op in operators:
        intermediate_result = op(a, b)
        if intermediate_result <= line.total:
            # print("\t"*indent, a, b, op, "continuing")
            # we still have room for some other operations
            intermediate_line = Line(line.total, [intermediate_result] + line.operands[2:])
            # following_operators = evaluate(intermediate_line, operators, indent+1)
            following_operators = evaluate(intermediate_line, operators)
            if following_operators:
                # subsequent calculations managed to arrive to the total! yay!
                return [op] + following_operators
            else:
                # skip - the choice of this operator did not help create a correct equation
                # print("\t"*indent, "didn't work")
                continue
        elif intermediate_result > line.total:
            # skip - we overshoot, so it's no use to continue
            # print("\t"*indent, a, b, op, "overshoot")
            continue
        # elif intermediate_result == line.total:
        #     if len(line.operands) > 2:
        #         # skip - we somehow reached the total, but we didn't use all numbers, so we did something wrong
        #         print("\t"*indent, a, b, op, "equal but before consuming every digit")
        #         continue
        #     elif len(line.operands) == 2:
        #         # good case!
        #         return [op]
        #     else:
        #         raise Exception("no fugging way")
    else:
        # we reach this part if no good cases have been found
        return None 

OPERATORS = [
    (operator.add, "+"),
    (operator.mul, "*")
]

def main(args):
    lines: List[Line] = parse(args.fname)

    sum_of_obtainables = 0
    for line in lines:

        if functools.reduce(operator.mul, line.operands) < line.total:
            print(line, "will always be wrong")
            continue
        
        list_of_operators = evaluate(line, [op for op, _ in OPERATORS])
        can_be_obtainable = bool(list_of_operators)
        if can_be_obtainable:
            print(line , "-->", list_of_operators)
            sum_of_obtainables += line.total
        else:
            print("wrong expression", line)
    print("total", sum_of_obtainables)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())