import flywheel
import re
import sys
import os
import glob
import shutil


def rename_bids(args):
    
    for root, subdirs, files in os.walk("/storage/ttapera/RBC/data/{}/".format(args[1])):

        for f in files:
            if args[1] in f:
                print("renaming file ", f)
                new_name = f.replace(args[1], args[2])
                print(new_name)
                os.rename(root + "/" + f, root + "/" + new_name)
    
    old_name = "/storage/ttapera/RBC/data/{}/sub-{}".format(args[1], args[1])
    new_name = "/storage/ttapera/RBC/data/{}/sub-{}".format(args[1], args[2])
    print(new_name)
    shutil.move(old_name, new_name)


def main():
    
    # args: bblid, hash, full-id, process

    args = sys.argv
    rename_bids(args)

if __name__ == '__main__':
    main()