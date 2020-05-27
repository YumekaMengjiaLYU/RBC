import sys
import glob
import nibabel as nb

def check_download(path):

    print("Checking for successful download in ", path)
    
    paths = glob.glob(path)
    paths = paths[1:]
    for name in paths:

        print(name)
        try:
            img = nb.load(name)
        except Exception as e:
            print(e)
            return False

    return True

check = check_download("/storage/ttapera/RBC/data/test/sub-*/ses-*/*/*.nii.gz")

if check:
    print("All files ok!")
    sys.exit(0)
    
else:
    print("Files did not download correctly!")
    sys.exit(1)