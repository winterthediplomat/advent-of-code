import argparse
import functools
import time
import collections
import enum
import pprint
import copy
import math

class Direction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    NONE = 4

Position = collections.namedtuple("Position", ["x", "y", "direction"])

MAX_STEPS = 10_000 

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
            return mappa[pos_info.x-1][pos_info.y] in ["#", "O"]
        except IndexError:
            return False
        except AssertionError:
            return False
    elif pos_info.direction == Direction.DOWN:
        try:
            return mappa[pos_info.x+1][pos_info.y] in ["#", "O"]
        except IndexError:
            return False
        except AssertionError:
            return False
    elif pos_info.direction == Direction.LEFT:
        try:
            assert (pos_info.y - 1) >= 0 
            return mappa[pos_info.x][pos_info.y-1] in ["#", "O"]
        except IndexError:
            return False
        except AssertionError:
            return False        
    elif pos_info.direction == Direction.RIGHT:
        try:
            return mappa[pos_info.x][pos_info.y+1] in ["#", "O"]
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

def walk_until_point_of_interest(mappa, pos_info: Position):
    new_x, new_y = pos_info.x, pos_info.y 
    walked_on = []
    if pos_info.direction == Direction.UP:
        while new_x >= 0 and not has_obstacle_on_front(mappa, Position(new_x, new_y, pos_info.direction)):
            walked_on.append(Position(new_x, new_y, pos_info.direction)) 
            new_x = new_x - 1
    elif pos_info.direction == Direction.DOWN:
        while new_x < len(mappa) and not has_obstacle_on_front(mappa, Position(new_x, new_y, pos_info.direction)):
            walked_on.append(Position(new_x, new_y, pos_info.direction)) 
            new_x = new_x + 1
    elif pos_info.direction == Direction.RIGHT:
        while new_y < len(mappa[0]) and not has_obstacle_on_front(mappa, Position(new_x, new_y, pos_info.direction)):
            walked_on.append(Position(new_x, new_y, pos_info.direction)) 
            new_y = new_y + 1
    elif pos_info.direction == Direction.LEFT:
        while new_y >= 0 and not has_obstacle_on_front(mappa, Position(new_x, new_y, pos_info.direction)):
            walked_on.append(Position(new_x, new_y, pos_info.direction)) 
            new_y = new_y - 1
    return (Position(new_x, new_y, pos_info.direction), walked_on)


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

def symbol_by_dir(dir: Direction, step: int = None):
    dirsymbol = {
        Direction.DOWN: "v",
        Direction.LEFT: "<",
        Direction.RIGHT: ">",
        Direction.UP: "^"
    }[dir]

    if step == None:
        return dirsymbol
    else:
        global MAX_STEPS
        return str(step).rjust(math.ceil(math.log10(MAX_STEPS)), "0")+dirsymbol

def evolve(mappa, pos_info: Position, step: int = None, write: bool = False):
    if has_obstacle_on_front(mappa, pos_info):
        if write:
            mappa[pos_info.x][pos_info.y] = symbol_by_dir(pos_info.direction, step) 
        # current_value = mappa[pos_info.x][pos_info.y]
        new_direction = turn_right(pos_info.direction)
        return True, Position(pos_info.x, pos_info.y, new_direction)
    else:
        # current_value = mappa[pos_info.x][pos_info.y]
        new_position, walked_on = walk_until_point_of_interest(mappa, pos_info)
        out = is_out_of_bounds(mappa, new_position) 

        if write:
            for walk_step in walked_on:
                mappa[walk_step.x][walk_step.y] = symbol_by_dir(pos_info.direction, step) 
            mappa[pos_info.x][pos_info.y] = symbol_by_dir(pos_info.direction, step) 
        # print("out of bounds?", out, "new_pos", new_position)
        return (not out), new_position

def main(args):
    mappa, position_info = parse(args.fname)
    original_position_info = copy.deepcopy(position_info)
    
    # pprint.pprint(mappa)

    can_be_evolved = True
    step = None
    while can_be_evolved:
        # print(position_info)
        can_be_evolved, position_info = evolve(mappa, position_info, write=True)
        # step += 1

    # print("==>") 
    # pprint.pprint(mappa)
    
    possible_positions: list[Position] = []
    for i in range(len(mappa)):
        for j in range(len(mappa[0])):
            if mappa[i][j] in "123X^>v<":
                mappa[i][j] = "."
                possible_positions.append(Position(i, j, Direction.NONE)) 

            # if step != None:
            #     if mappa[i][j] == ".":
            #         mappa[i][j] = " . "
            #     elif mappa[i][j] == "#":
            #         mappa[i][j] = " # "

    print("---", len(possible_positions))

    obstacles = 0

    prev_candidate_pos = None
    for candidate_pos in possible_positions:
        obstacle_i, obstacle_j = candidate_pos.x, candidate_pos.y

        # aggiorna la mappa
        mappa[obstacle_i][obstacle_j] = "O"
        if prev_candidate_pos:
            mappa[prev_candidate_pos.x][prev_candidate_pos.y] = "."
        prev_candidate_pos = candidate_pos # salva posizione da ripristinare

        can_be_evolved = True
        steps = 0
        cycle_found = False
        position_info = copy.deepcopy(original_position_info)
        all_positions = set([position_info])
        debug_step = None
        while can_be_evolved and (steps < MAX_STEPS) and not cycle_found:
            # print(position_info)
            try:
                can_be_evolved, position_info = evolve(mappa, position_info, debug_step)

                if can_be_evolved:
                    if position_info in all_positions:
                        raise ValueError(position_info)
                    else:
                        all_positions.add(position_info)

                steps += 1
                # debug_step += 1
            except ValueError:
                cycle_found = True

        if steps == MAX_STEPS or cycle_found:
            print("obstacle can be put at ", candidate_pos, "steps: ", steps)

            # mappa_to_show = copy.deepcopy(mappa) 
            # for i in range(len(mappa)):
            #     for j in range(len(mappa[0])):
            #         if mappa[i][j] not in "#":
            #             mappa[i][j] = "."

                    # if mappa_to_show[i][j] in "#O.123":
                    #     mappa_to_show[i][j] = "{}{}{}".format(
                    #         " "*(math.ceil(math.log10(MAX_STEPS))//2),
                    #         mappa_to_show[i][j],
                    #         " "*(math.ceil(math.log10(MAX_STEPS))//2))
                # mappa_to_show[i] = "".join(mappa_to_show[i])
                # print(mappa_to_show[i])
            # pprint.pprint(mappa)

            # pprint.pprint(all_positions)

            obstacles += 1
        else:
            for i in range(len(mappa)):
                for j in range(len(mappa[0])):
                    if mappa[i][j] not in "#":
                        mappa[i][j] = "."
 
        all_positions = [] 
    
    print("possible positions", obstacles)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())