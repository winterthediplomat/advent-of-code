import argparse
import collections
#from types import List
import functools
import operator
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
    if len(line.operands) == 1:
        if line.operands[0] == line.total:
            raise Exception("how tf")
        else:
            return None

    a, b = line.operands[:2]
    for op in operators:
        intermediate_result = op(a, b)
        if intermediate_result < line.total:
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
                # skip - we somehow reached the total, but we didn't use all numbers, so we did something wrong
                continue
            elif len(line.operands) == 2:
                # good case!
                return [op]
            else:
                raise Exception("no fugging way")
    else:
        # we reach this part if no good cases have been found
        return None 

OPERATORS = [
    (operator.mul, "*"),
    (operator.add, "+")
]


@functools.cache
def base_3_convert(num):
    result = ""
    while num > 0:
        num, remainder = num // 3, num % 3
        result = str(remainder) + result
    return result

def main(args):
    lines: List[Line] = parse(args.fname)

    sum_of_obtainables = 0
    for line in lines:

        can_be_obtainable = False
        operators_spots = len(line.operands)-1
        for idx in range(3**operators_spots):
            mapping = base_3_convert(idx).rjust(operators_spots, "0")
            
            intermediate_value = line.operands[0] 
            for mapping_idx, digit in enumerate(mapping):
                operand_idx = mapping_idx+1
                if digit == "0":
                    intermediate_value = intermediate_value + line.operands[operand_idx]
                elif digit == "1":
                    intermediate_value = intermediate_value * line.operands[operand_idx]
                elif digit == "2":
                    other = line.operands[operand_idx]
                    # small constant added to avoid special-casing other=1, 10, 100, ...
                    shift = math.ceil(math.log10(other+0.0000001))
                    intermediate_value = (intermediate_value * 10**shift) + other
            
            if intermediate_value == line.total:
                can_be_obtainable = True
                list_of_operators = mapping
                break

        # list_of_operators = evaluate(line, [op for op, _ in OPERATORS])
        # can_be_obtainable = bool(list_of_operators)
        if can_be_obtainable:
            # print(line, "-->", list_of_operators)
            sum_of_obtainables += line.total
        else:
            pass # print("wrong expression", line)
    print("total", sum_of_obtainables)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())