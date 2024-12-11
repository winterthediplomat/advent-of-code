import argparse
from collections import namedtuple
import itertools
import math

FileData = namedtuple("FileData", ["ident", "size", "space_after"])

def parse(fname):
    result = []

    with open(fname) as src:
        line = src.read()
        line = line.strip()

    for idx, fd in enumerate(itertools.batched(line, 2)):
        try:
            size, space_after = fd
        except ValueError:
            size, space_after = fd[0], 0

        result.append(FileData(idx, int(size), int(space_after)))

    return result


def get_farthest_of_size(cache_of_sizes, to_be_filled):
    try:
        return cache_of_sizes[to_be_filled][-1]
    except IndexError:
        # the array is empty
        return None
    except KeyError:
        # there is no file as big as `to_be_filled` (not likely with larger imputs) 
        return None

def main(args):
    full_mapping = parse(args.fname)

    # keep a set of files we've moved, that can
    # be skipped while searching - we already moved it,
    # and already calculated its checksum
    min_defrag = set()

    # max identifier is the last file - we want to stop
    # when the file we are trying to move is the last
    max_ident = -1

    # create a small cache
    cache_of_sizes = {0: []}
    for fd in full_mapping:
        max_ident = fd.ident
        # print("*", fd)
        try:
            cache_of_sizes[fd.size].append(fd.ident)
        except KeyError:
            cache_of_sizes[fd.size] = [fd.ident]

    # print(cache_of_sizes)

    checksum = 0
    pos = 0
    for fd in full_mapping:
        # did we reach the last file?
        if fd.ident == max_ident:
            # (maybe, if the last file wasn't moved, the checksum
            # does not contain this file - never happened on our
            # inputs, though)
            print("completed")
            continue

        if fd.ident in min_defrag:
            # we have already moved this file, so we have to skip
            # its space
            pos += fd.size
        else:
            # calculate the checksum of this file...
            added = sum((pos+i)*fd.ident for i in range(fd.size))
            # ... add it to the global checksum...
            checksum += added
            # ...and move the pos cursor over
            pos += fd.size

        # now, let's start filling the space after the file
        space_between = fd.space_after
        can_try_searching = True
        how_filled = 0

        while can_try_searching:
            # let's search the highest file ID (most distant) that can fit in the free space after the file
            # get_farthest_of_size: size -> identifier | None
            all_farthest_sizes = list(sorted(filter(lambda x: x[0], map(lambda s: (get_farthest_of_size(cache_of_sizes, s), s), range(space_between+1))), reverse=True))
            try:
                # let's get the file ID to put here
                # if no candidate is found, an IndexError will be thrown, and the search will be stopped
                # (no file can be put here)
                rw_ident, chosen_size = all_farthest_sizes[0]

                # let's check if we are trying to move a file to the end of "hard drive"
                # we don't want to do that, we already calculated this file's checksum
                assert rw_ident > fd.ident

                # the chosen file (rw_ident) cannot be moved anymore
                cache_of_sizes[chosen_size].pop()
                # let's keep track of the fact we moved it
                min_defrag.add(rw_ident)
                # calculate the checksum
                added = sum((pos+i)*rw_ident for i in range(chosen_size))
                checksum += added 
                pos += chosen_size 
                # ...and update the remaining space, so we can verify that there is room for other files too
                how_filled += chosen_size 
                space_between = fd.space_after - how_filled
                can_try_searching = (space_between > 0) and (fd.space_after > how_filled) 
            except AssertionError:
                # as said before, we were trying to move a file to the end, and it is not ok
                can_try_searching = False
            except IndexError:
                # no suitable file has been found :(
                can_try_searching = False 
        # update the pos cursor to the start of the new file 
        pos += (fd.space_after - how_filled) 

    print("checksum", checksum)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())
