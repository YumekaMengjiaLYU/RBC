import flywheel
import re
import sys
import os
import glob
import shutil
import subprocess
import nibabel as nb
from fw_heudiconv.cli import export


client = flywheel.Client()

RBC_proj = client.projects.find_first('label="ReproBrainChart"')

RBC_subjects = RBC_proj.subjects()

PNC_CS_proj = client.projects.find_first('label="PNC_CS_810336"')
PNC_LG_proj = client.projects.find_first('label="PNC_LG_810336"')

#PNC_CS_subjects = PNC_CS_proj.subjects()
#PNC_LG_subjects = PNC_LG_proj.subjects()


# function to remove a subject from the RBC project
def remove_current_rbc_subject(args, RBC_subjects=RBC_subjects):

    target = [x for x in RBC_subjects if x.label == args[3]]
    if len(target) == 1:
        print('found subject to remove: ', args[3], target[0].id)
        client.delete_subject(target[0].id)
        return True
    else:
        return False


def download_bids2(args):
    
    # use the fw export bids cli + subprocess to download the anat fmap and func folders
    print("Gathering PNC BIDS...")

    processes = []
    
    processes.append("fw export bids /storage/ttapera/RBC/data/{}/bids_dataset --project PNC_CS_810336 --subject {} --data-type anat".format(args[2], str(args[1])))
    
    processes.append("fw export bids /storage/ttapera/RBC/data/{}/bids_dataset --project PNC_CS_810336 --subject {} --data-type func".format(args[2], str(args[1])))
    
    processes.append("fw export bids /storage/ttapera/RBC/data/{}/bids_dataset --project PNC_CS_810336 --subject {} --data-type fmap".format(args[2], str(args[1])))

    # use subprocess just to see which download successfully; those without PNC_LG will fail with exit 1
    statuses = []
    
    for i, process in enumerate(processes):
        os.makedirs('/storage/ttapera/RBC/data/{}/bids_dataset'.format(args[2]), exist_ok=True)
        stat = os.system(process)
        if int(stat) == 1:
            print("Failed export:\n", i)
        else:
            print("Process ", i, " complete with status ", stat)



def cleanup_bids(path):
    
    # Remove any files from PNC2/3 that are not 
    paths = glob.glob(path)
    paths = paths[1:]

    for name in paths:

        print(name)
        pattern = re.compile("sub-[0-9]+_ses-PNC[^1]+_task-[^(rest)]")
        if pattern.search(name):
            print("removing file...")
            os.system("rm {}".format(name))


def rename_bids(args):
    
    for root, subdirs, files in os.walk("/storage/ttapera/RBC/data/{}/bids_dataset/".format(args[2])):

        for f in files:
            if args[1] in f:
                print("renaming file ", f)
                new_name = f.replace(args[1], args[2])
                os.rename(root + "/" + f, root + "/" + new_name)
    
    old_name = "/storage/ttapera/RBC/data/{}/bids_dataset/sub-".format(args[2]) + args[1]
    new_name = old_name.replace(args[1], args[2])
    shutil.move(old_name, new_name)


def check_headers(path):

    print("Checking for successful download in ", path)
    
    paths = glob.glob(path)
    paths = paths[1:]
    if len(paths) <= 1:
        return False
    for name in paths:
        if any([x in name for x in [".json", ".bvec", ".bval"]]):
            continue
        print(name)
        try:
            img = nb.load(name)
        except Exception as e:
            print(e)
            return False

    return True


def main():
    
    # args: bblid, hash, full-id, process

    args = sys.argv
    path = "/storage/ttapera/RBC/data/{}/bids_dataset/sub-*/ses-*/*/*".format(args[2])

    subject_removed = remove_current_rbc_subject(args)
    if subject_removed:
        print("Removed subject.")

    download_bids2(args)
    #cleanup_bids(path)
    rename_bids(args)
    check = check_headers(path)
    if check:
        print("Done!")
        sys.exit(0)
    else:
        print("Warning: Download may not have completed successfully!")
        sys.exit(1)


if __name__ == '__main__':
    main()