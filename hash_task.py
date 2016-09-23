import sys
import os
import hashlib

from collections import defaultdict

dir = defaultdict(list)

def make_hash(filename):
    size = 1024
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        buf = f.read(size)
        while buf:
            hash_md5.update(buf)
            buf = f.read(size)
    return hash_md5.hexdigest()

def show_dic():
    for v in dir.values():
        if len(v) > 1:
            print(":".join(v))


def find_dubl(arg):
    for path in sys.argv[1:]:
        for root, _, files in os.walk(path):
            for name in files:
                if name[0] != "." and name[0] != "~":
                    file_path = os.path.join(root, name)
                    path = os.path.abspath(file_path)
                    if not os.path.islink(file_path):
                      dir[make_hash(file_path)].append(path)

def main():
    find_dubl(sys.argv)
    show_dic()

if __name__ == "__main__":
    main()
