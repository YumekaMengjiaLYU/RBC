import flywheel
import glob
import os
import pathlib
import re
import json
import sys


client = flywheel.Client()


def get_subject_session(f):
    # use regex to look for the subject label and session label
    
    sub_search = re.search(r'sub-[a-zA-Z0-9]+', f)

    assert sub_search.group(0)

    subject = sub_search.group(0)


    ses_search = re.search(r'ses-[a-zA-Z0-9]+', f)

    assert ses_search.group(0)

    session = ses_search.group(0)

    # retun as a tuple
    return(subject, session)


def create_acquisition_label(f):

       
    # get the subject and session labels so that we can insert them into a regex search string
    subject, session = get_subject_session(f)

    # use pathlib to get the stem (filename without slashes and extensions)
    stem = pathlib.Path(f).stem    
    
    # sometimes we need to keep removing extensions, e.g. 'file.nii.gz'; use a while loop
    while '.' in stem:
        stem = pathlib.Path(stem).stem

    # remove the word 'context' from the stem
    if 'context' in stem:
        stem = stem[:-7]
    
    # create the regex search string
    regex = '(?<={}_{}_).+'.format(subject, session)

    # run regex
    acquisition_label = re.search(regex, stem).group(0)
    return(acquisition_label)


def build_metadata(file_list):
    # build a dictionary of metadata to add to the file
    
    # get the json file and nifti file from this acquisition
    json_file = [f for f in file_list if f.endswith('.json')][0]
    nifti_file = [f for f in file_list if '.nii' in f][0]

    # open it
    with open(json_file, 'r') as read_file:
            json_data = json.load(read_file)

    # add important BIDS fields
    bids = {
        'Acq': '',
        'Dir': '',
        'Filename': '',
        'Folder': '',
        'ignore': False,
        'Modality': '',
        'Path': '',
        'Run': ''
    }

    # to fill these BIDS fields, we extract them from the filename:
    def find_value(string, key):

        regex = r'(?<={}-)[a-zA-Z0-9]+'.format(key)

        target_key = re.search(regex, string)

        try:
            return target_key.group(0)
        except:
            return ''

    bids['Acq'] = find_value(nifti_file, 'acq')
    bids['Dir'] = find_value(nifti_file, 'dir')
    bids['Run'] = find_value(nifti_file, 'run')

    bids['Filename'] = pathlib.Path(nifti_file).name
    bids['Folder'] = pathlib.Path(nifti_file).parents[0].name
    bids['Path'] = '/'.join(list(pathlib.Path(nifti_file).resolve().parts[-4:-1]))
    mod = create_acquisition_label(pathlib.Path(nifti_file).stem)
    bids['Modality'] = mod[mod.find('_')+1:]
    
    json_data['BIDS'] = bids
    return(json_data)


def check_acquisitions(acq_dict):
    
    for k,v in acq_dict.copy().items():
        
        if not any(['.nii' in x for x in v]):
            del acq_dict[k]
    
    return(acq_dict)


def build_and_upload_asl(args):
    
    # step 1: get files
    
    path = '/storage/ttapera/RBC/data/{}/*/*/*/*'.format(args[1])
    files = glob.glob(path)
    
    print('Available files:\n',files)
    # step 2: get the asl acquisitions
    acquisitions = {}

    for f in files:

        acq = create_acquisition_label(f)

        # if the key does not exist, create it and assign the value as a list with this file
        if acq not in acquisitions.keys():
            acquisitions[acq] = [f]
        # otherwise, if the key exists, append the file to that list of files
        else:
            acquisitions[acq].append(f)
    
    # ensure correct files are present
    acquisitions = check_acquisitions(acquisitions)
    
    assert acquisitions
    # step 3: extract subject and session labels; initialise flywheel target object
    
    print(acquisitions)
    subject, session = get_subject_session(files[0])

    project = client.projects.find_first('label=RBC_PNC')
    subject = project.subjects.find_first('label={}'.format(subject))
    session = subject.sessions.find_first('label={}'.format(session))
    
    # step 4: upload data
    
    for k,v in acquisitions.items():
        print()
        print('Processing acquisition:', k)

        new_acquisition = session.add_acquisition(label="{}".format(k))

        print('Building acquisition metadata')

        meta = build_metadata(v)

        for file_upload in v:

            # we no longer need to upload jsons
            if '.json' in file_upload:
                continue

            # upload TSVs straight to the session object
            elif 'context' in file_upload:
                print('Updating TSV metadata...')
                # the context file doesn't need as much data, 
                # just the BIDS Filename, Path, and Folder
                subset_meta = meta['BIDS'].copy()
                subset_meta['Filename'] = subset_meta['Filename'].replace('asl.nii.gz', 'aslcontext.tsv')

                print('Uploading TSV to session')
                session.upload_file(file_upload)
                session = session.reload()
                session.update_file_info(subset_meta['Filename'], {'BIDS': subset_meta})
                session = session.reload()

            # upload the nifti to the new acquisition
            elif '.nii' in file_upload:
                print('Uploading file ', file_upload)
                new_acquisition.upload_file("{}".format(file_upload))
                new_acquisition = new_acquisition.reload() # update your copy of the object

                # update the metadata
                print('Updating nifti metadata...')
                new_acquisition.update_file_info(meta['BIDS']['Filename'], meta)
                new_acquisition = new_acquisition.reload() # update your copy of the object


        print()
        

def main():
    
    args = sys.argv
    build_and_upload_asl(args)
    

if __name__ == '__main__':
    main()