import argparse
import collections
import itertools

FileData = collections.namedtuple("FileData", ["ident", "size", "space_after"])

def parse(fname):
    result = []
    full_compressed_size = 0
    whole_size = 0

    with open(fname) as src:
        line = src.readline().strip()

    for ident, file_data in enumerate(itertools.batched(line, n=2)):
        try:
            size, space = int(file_data[0]), int(file_data[1])
        except IndexError: # batched may return (x, ) if line len is odd
            size, space = int(file_data[0]), 0

        full_compressed_size += size
        whole_size += size + space
        result.append(FileData(ident, size, space))

    return result, full_compressed_size, whole_size

def main(args):
    full_mapping, fully_compressed_size, whole_size = parse(args.fname)

    fw_iter = iter(full_mapping)
    rw_iter = reversed(full_mapping)

    space_at_end = 0
    current_pos = 0
    checksum = 0
    space_between_files: int = 0 
    debug_mem = ""

    fw_file: FileData = None
    rw_file: FileData = None
    while (current_pos < fully_compressed_size):
        if not rw_file:
            rw_file = next(rw_iter)
            # print("rw file", rw_file)
            space_at_end += rw_file.space_after

            
        if space_between_files == 0:
            fw_file = next(fw_iter)
            if fw_file.ident == rw_file.ident:
                # print("reached same file from both iterators!", fw_file, rw_file,
                #       "writing the remaining part of rw_file")
                checksum += sum((current_pos+i)*rw_file.ident for i in range(rw_file.size))
                # debug_mem += str(rw_file.ident)*rw_file.size

                break
            # print("adding fw file", fw_file)
            space_between_files = fw_file.space_after
            checksum += sum((current_pos+i)*fw_file.ident for i in range(fw_file.size))
            current_pos += fw_file.size
            # debug_mem += str(fw_file.ident)*fw_file.size

        if space_between_files < rw_file.size:
            # need more space to store the rw file
            # print("writing a chunk of rw ", rw_file, end=" ") 
            checksum += sum((current_pos+i)*rw_file.ident for i in range(space_between_files))
            current_pos += space_between_files
            # debug_mem += str(rw_file.ident)*space_between_files

            # space_after = 0, already counted in space_at_end
            rw_file = FileData(rw_file.ident, rw_file.size - space_between_files, 0)
            # print(", converted to", rw_file)
            space_at_end += space_between_files
            space_between_files = 0 
            # leggiamo il prossimo file fw
            fw_file = None
        elif space_between_files > rw_file.size:
            # we have space for other files
            # print("completing copy of rw_file", rw_file, "with remaining space to fill")
            checksum += sum((current_pos+i)*rw_file.ident for i in range(rw_file.size))
            current_pos += rw_file.size
            # debug_mem += str(rw_file.ident)*rw_file.size

            space_at_end += rw_file.size 
            space_between_files = space_between_files - rw_file.size
            rw_file = None
        elif space_between_files == rw_file.size:
            # print("fully fill space with rw", rw_file)
            # enough space to complete the copy of rw file 
            checksum += sum((current_pos+i)*rw_file.ident for i in range(space_between_files))
            current_pos += space_between_files
            space_at_end += rw_file.size 
            # debug_mem += str(rw_file.ident)*space_between_files

            space_between_files = 0
            fw_file = None
            rw_file = None
    
    # debug_mem += "."*space_at_end 
    # print("debug mem", debug_mem)
    print("checksum", checksum) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fname")
    main(parser.parse_args())