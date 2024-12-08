import argparse
import functools
import time
import collections
import enum
import pprint

class Direction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

Position = collections.namedtuple("Position", ["x", "y", "direction"])

def parse(fname):
    mappa = []
    position_info = None 

    with open(fname) as src:
        for line in src:
            line = line.strip()
            up = line.find("^")
            right = line.find(">")
            down = line.find("v")
            left = line.find("<")
            
            if up != -1:
                position_info = Position(len(mappa), up, Direction.UP)
            elif right != -1:
                position_info = Position(len(mappa), right, Direction.RIGHT)
            elif down != -1:
                position_info = Position(len(mappa), down, Direction.DOWN)
            elif left != -1:
                position_info = Position(len(mappa), left, Direction.LEFT)

            line = list(line)
            mappa.append(line)

    return mappa, position_info

def has_obstacle_on_front(mappa, pos_info):
    if pos_info.direction == Direction.UP:
        try:
            assert (pos_info.x - 1) >= 0 
            return mappa[pos_info.x-1][pos_info.y] == "#"
        except IndexError:
            return False
        except AssertionError:
            return False
    if pos_info.direction == Direction.DOWN:
        try:
            return mappa[pos_info.x+1][pos_info.y] == "#"
        except IndexError:
            return False
        except AssertionError:
            return False
    if pos_info.direction == Direction.LEFT:
        try:
            assert (pos_info.y - 1) >= 0 
            return mappa[pos_info.x][pos_info.y-1] == "#"
        except IndexError:
            return False
        except AssertionError:
            return False        
    if pos_info.direction == Direction.RIGHT:
        try:
            return mappa[pos_info.x][pos_info.y+1] == "#"
        except IndexError:
            return False
        except AssertionError:
            return False
        
def turn_right(direction):
    return {
        Direction.UP: Direction.RIGHT,
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.UP
    }[direction]

def walk(pos_info: Position):
    return {
        Direction.UP: lambda pos: Position(pos.x-1, pos.y, Direction.UP),
        Direction.DOWN: lambda pos: Position(pos.x+1, pos.y, Direction.DOWN),
        Direction.LEFT: lambda pos: Position(pos.x, pos.y-1, Direction.LEFT),
        Direction.RIGHT: lambda pos: Position(pos.x, pos.y+1, Direction.RIGHT),
    }[pos_info.direction](pos_info)

def is_out_of_bounds(mappa, new_position):
    try:
        assert new_position.x >= 0
        assert new_position.y >= 0
        _ = mappa[new_position.x][new_position.y]
        return False 
    except IndexError:
        return True 
    except AssertionError:
        return True 

def evolve(mappa, pos_info: Position):
    if has_obstacle_on_front(mappa, pos_info):
        mappa[pos_info.x][pos_info.y] = "X"
        new_direction = turn_right(pos_info.direction)
        return True, Position(pos_info.x, pos_info.y, new_direction)
    else:
        mappa[pos_info.x][pos_info.y] = "X"
        new_position = walk(pos_info)
        out = is_out_of_bounds(mappa, new_position) 
        # print("out of bounds?", out, "new_pos", new_position)
        return (not out), new_position

def main(args):
    mappa, position_info = parse(args.fname)

    can_be_evolved = True
    while can_be_evolved:
        print(position_info)
        can_be_evolved, position_info = evolve(mappa, position_info)
    
    steps = 0
    for i in range(len(mappa)):
        for j in range(len(mappa[0])):
            if mappa[i][j] == "X":
                steps += 1

        mappa[i] = "".join(mappa[i])

    pprint.pprint(mappa)
    print("steps: ", steps) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())