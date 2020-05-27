import flywheel
import re
import sys
import os
import glob
import shutil
import nibabel as nb
from fw_heudiconv.cli import export

client = flywheel.Client()

def download_bids(args):

    sessions = None
    
    print("Gathering PNC CS BIDS...")
    pnc1_data = export.gather_bids(client, "PNC_CS_810336", args[1], sessions)
    print("\nDownloading BIDS...\n")
    export.download_bids(
        client, pnc1_data, 
        '/storage/ttapera/RBC/data/', 
        folders_to_download = ['anat', 'func', 'fmap'],
        dry_run=False)

    #print("Gathering PNC LG BIDS...")
    #try:
    #    pnc2_data = export.gather_bids(client, "PNC_LG_810336", args[1], sessions)

    #    export.download_bids(
    #        client, pnc2_data, 
    #        '/storage/ttapera/RBC/data/', 
    #        folders_to_download = ['anat', 'func', 'fmap'],
    #        dry_run=False,
    #        name='PNC2')
    #except:
    #    print("no second session!")
        
    # merge any and all data
    #print("n\Merging\n")
    #os.system("cp -r -R /storage/ttapera/RBC/data/PNC*/* /storage/ttapera/RBC/data/upload/")

    # rename the files:
    #print("\nRenaming\n")
    #for root, subdirs, files in os.walk("/storage/ttapera/RBC/data/bids_dataset/"):

    #    for f in files:
    #        if args[1] in f:
    #            print("renaming file ", f)
    #            new_name = f.replace(args[1], args[2])
    #            os.rename(root + "/" + f, root + "/" + new_name)

    # rename the subject-level directory
    #old_name = "/storage/ttapera/RBC/data/bids_dataset/sub-" + args[1]
    #new_name = old_name.replace(args[1], args[2])
    #shutil.move(old_name, new_name)        
    #os.system("rm -rf /storage/ttapera/RBC/data/bids_dataset/sub*/sub*")
    

def download_bids2(args):

    print("Gathering PNC CS BIDS...")
    #pnc1_data = export.gather_bids(client, "PNC_CS_810336", args[1], sessions)
    #print("\nDownloading BIDS...\n")
    #export.download_bids(
    #    client, pnc1_data,
    #    '/storage/ttapera/RBC/data/',
    #    folders_to_download = ['anat', 'func', 'fmap'],
    #    dry_run=False,
    #    name='PNC1')
    os.system("mkdir /storage/ttapera/RBC/data/bids_dataset")
    os.system("fw export bids /storage/ttapera/RBC/data/bids_dataset --project PNC_CS_810336 --subject {}".format(str(args[1]))) 

    # rename the files:
    print("\nRenaming\n")
    for root, subdirs, files in os.walk("/storage/ttapera/RBC/data/bids_dataset/"):

        for f in files:
            if args[1] in f:
                print("renaming file ", f)
                new_name = f.replace(args[1], args[2])
                os.rename(root + "/" + f, root + "/" + new_name)

    # rename the subject-level directory
    old_name = "/storage/ttapera/RBC/data/bids_dataset/sub-" + args[1]
    new_name = old_name.replace(args[1], args[2])
    shutil.move(old_name, new_name)


# function to remove a subject from the RBC project
def remove_current_rbc_subject(args):
    
    RBC_proj = client.projects.find_first('label="ReproBrainChart"')
    RBC_subjects = RBC_proj.subjects()

    target = [x for x in RBC_subjects if x.label == args[3]]
    if len(target) == 1:
        print('found subject to remove: ', target[0].id)
        client.delete_subject(target[0].id)
        return True
    else:
        return False

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
        
def main():
    
    subject_removed = remove_current_rbc_subject(sys.argv)
    if subject_removed:
        print("Removed subject.")

    successful_download=False
    tries = 1
    max_tries = 25
    while not successful_download:
        
        if tries == max_tries:
            break
        else:
            tries += 1
        os.system('rm -rf /storage/ttapera/RBC/data/bids_dataset/*')
        download_bids2(sys.argv)

        successful_download = check_download('/storage/ttapera/RBC/data/bids_dataset/sub-*/ses-*/*/*.nii.gz')
    print("Downloading complete in " + str(tries) + " tries.")

    if tries >= max_tries:
        print("WARNING: Files may be corrupt!")


if __name__ == '__main__':
    main()
