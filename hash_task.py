import sys
import os
import hashlib

#def made_hash(filename):
#    size = 65536
#    hash_md5 = hashlib.md5()
#    with open(filename, "rb") as f:
#        buf = f.read(size)
#        while len(buf) > 0:
#            hash_md5.update(buf)
#            buf = f.read(size)
#    return hash_md5.hexdigest()

def made_hash(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        hash_md5.update(f.read())
    return hash_md5.hexdigest()


def main():
    dir = {}
    for path in sys.argv[1:]:
       for root, dirs, files in os.walk(path):
            for name in files:
              file_path = os.path.join(root, name)
              file_hash = made_hash(file_path)
              if file_hash not in dir:
                dir[file_hash] = []
              dir[file_hash].append(file_path)
    for v in dir.values():
        for file in v:
          print(file + ":")


if __name__ == "__main__":
    main()
