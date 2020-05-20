import flywheel
import re
import sys
import os
import glob
import shutil
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
        dry_run=False,
        name='PNC1')

    print("Gathering PNC LG BIDS...")
    try:
        pnc2_data = export.gather_bids(client, "PNC_LG_810336", args[1], sessions)

        export.download_bids(
            client, pnc2_data, 
            '/storage/ttapera/RBC/data/', 
            folders_to_download = ['anat', 'func', 'fmap'],
            dry_run=False,
            name='PNC2')
    except:
        print("no second session!")
        
    # merge any and all data
    print("n\Merging\n")
    os.system("cp -r -R /storage/ttapera/RBC/data/PNC*/* /storage/ttapera/RBC/data/upload/")

    # rename the files:
    print("\nRenaming\n")
    for root, subdirs, files in os.walk("/storage/ttapera/RBC/data/upload/"):

        for f in files:
            if args[1] in f:
                print("renaming file ", f)
                new_name = f.replace(args[1], args[2])
                os.rename(root + "/" + f, root + "/" + new_name)

    # rename the subject-level directory
    old_name = "/storage/ttapera/RBC/data/upload/sub-" + args[1]
    new_name = old_name.replace(args[1], args[2])
    shutil.move(old_name, new_name)        
    os.system("rm -rf /storage/ttapera/RBC/data/upload/sub*/sub*")
    


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

        
def main():
    
    subject_removed = remove_current_rbc_subject(sys.argv)
    if subject_removed:
        print("Removed subject.")
    download_bids(sys.argv)
    

if __name__ == '__main__':
    main()
