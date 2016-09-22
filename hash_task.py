import sys
import os
import hashlib

def made_hash(filename):
    size = 1024
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        buf = f.read(size)
        while len(buf) > 0:
            hash_md5.update(buf)
            buf = f.read(size)
    return hash_md5.hexdigest()

def main():
    dir = {}
    for path in sys.argv[1:]:
       for root, dirs, files in os.walk(path):
            for name in files:
                if name[0] != "." and name[0] != "~":
                  file_path = os.path.join(root, name)
                  file_hash = made_hash(file_path)
                  if file_hash not in dir:
                    dir[file_hash] = []
                  dir[file_hash].append(file_path)
    for v in dir.values():
        if len(v) > 1:
            for file in v:
              print(file,end = ":")
            print("")


if __name__ == "__main__":
    main()
