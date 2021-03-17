#!/usr/bin/env python

# QSIPREP AUDIT

# command line: python audit_script.py pipeline bids_dir output_dir error_dir audit_path

from pathlib import Path
import pandas as pd
import numpy as np
import json
import sys
import os
from bs4 import BeautifulSoup
import glob
import os
import subprocess
import pdb 
import time

def get_sub_name(path):
    parts = path.parts
    for part in parts:
        if part.startswith("sub-"):
            return part

pipeline = sys.argv[1]

bids_dir = sys.argv[2]

# bids_dir = '/Users/scovitz/abcddlsubs'

output_dir = sys.argv[3]

# output_dir = '/Users/scovitz/abcdqsiprepsubs'

error_dir = sys.argv[4]

# check for a rerun
rerun = False
if len(sys.argv) == 8:
    rerun = True
    # error dir for rerun subs
    rerun_error_dir = sys.argv[6]
    print("RERUN ERROR DIR", rerun_error_dir) 
    # get list of rerun subs 
    rerun_txt = open(sys.argv[7], "r")
    rerun_subs = rerun_txt.readlines()
    for i in range(len(rerun_subs)):
        rerun_subs[i] = rerun_subs[i].strip("\n")
    rerun_txt.close()
print("NUM RERUN SUBS", len(rerun_subs))

# GET LIST OF ALL BRANCH NAMES
# CREATE DICTIONARY OF SUB_ID/BRANCH_NAME KEY/VALUE PAIRS
sp = subprocess.Popen(["git", "branch", "-l"], stdout=subprocess.PIPE, cwd=output_dir)
branches = sp.stdout.readlines()
sub_branch_names = {}
for branch in branches:
    branch_name = branch.strip()
    branch_name = str(branch_name)
    branch_name = branch_name[2:len(branch_name)-1]
    if branch_name.startswith("sub-"):
        sub_branch_names[branch_name[:-8]] = branch_name

# save list of branch names
# save list of subject names 
output_subs = sub_branch_names.keys()

# Get all bids dir subs and add them to the csv 
sub_ids = []
sub_paths = []

for path in Path(bids_dir).glob("sub-*"):
    sub_id = get_sub_name(path)
    if rerun == True:
        if sub_id in rerun_subs: 
            sub_ids.append(sub_id)
            sub_paths.append(str(path))
    else:
        sub_ids.append(sub_id)
        sub_paths.append(sub_path)
if pipeline == "qsiprep":
    columns = ["SubjectID", "HasOutput", "HasHTML", "NoErrorsToReport", "ProducedPreprocessedDWIs", "ProducedPreprocesedANATs", "RanT1wSpatialNormalization", "HasDwiDir", "HasFmapDir", "AllFmapsHaveIntendedFors", "NoMissingDwiPhaseEncodingDirection", "NoMissingFmapPhaseEncodingDirection", "ErrorDescription"]

if pipeline == "fmriprep":
    columns = ["SubjectID", "HasOutput", "HasHTML", "NoErrorsToReport", "HasFuncDir",
            "HasBold", "ProducedFuncDir", "RanSurfBold", "RanVolBold", "HasErrorFile",
            "RuntimeErrorDescription", "OSErrorDescription", "CommandErrorDescription",
            "HadScratchSpace", "HadRAMSpace", "HadDiskSpace", "FinishedSuccessfully"]


audit = pd.DataFrame(np.nan, index=range(0,len(sub_ids)), columns=columns, dtype="string")

audit["Path"] = sub_paths
audit["SubjectID"] = sub_ids

cntr = 0
for row in range(len(audit)):
    cntr += 1
    # get output branch name for input dir 
    # if it doesn't exist, then HasOutput = False!
    subject = audit.iloc[row]["SubjectID"]
    if subject in output_subs:
        # need to checkout to the subject specific branch! 
        # subproces.call IS BLOCKING (necessary!)
        msg = subprocess.call(["git", "checkout", sub_branch_names[subject]], stdout=subprocess.PIPE, cwd=output_dir)
        print(cntr)
        if msg != 0:
            print("On branch ", sub_branch_names[subject])
            print("Checkout error code: ", msg)
        
        # ON BRANCH, CHECK IF OUTPUT DIR GOT CREATED 
        if Path(output_dir + "/" + subject).exists:
            audit.at[row, "HasOutput"] = "True"
        else:
            audit.at[row, "HasOutput"] = "False"
    
    # IN THE CASE OF NO BRANCH CREATED
    else:
        audit.at[row, "HasOutput"] = "False"
        audit.at[row, "ProducedFuncDir"] = "False"
        audit.at[row, "RanSurfBold"] = "False"
        audit.at[row, "RanVolBold"] = "False"
    
    # NOT PIPELINE SPECIFIC
    
    # need to checkout to the subject specific branch! 
    #subprocess.Popen(["git", "checkout", names[0]], cwd='/cbica/projects/RBC/PNC_fmriprep/fmriprep')

    # check if output subject dir got generated
    #if Path(output_dir + "/" + audit.iloc[row]["SubjectID"]).exists():
    #    audit.at[row, "HasOutput"] = "True"
    #else:
    #    audit.at[row, "HasOutput"] = "False"
    #    print(audit.iloc[row]["SubjectID"])
        #continue 

    # check if html file got generated
    # CHANGE THIS LINE TO USE (IPYTHON TEST IF WORKS FIRST!)
    # glob.glob('%s/*%s*.e*'%(output_dir,subject)),key=os.path.getmtime)[-1]
    html_filename = output_dir + "/" + subject + ".html"
    #print(html_filename)
    if Path(html_filename).exists():
        audit.at[row, 'HasHTML'] = "True"

        soup = BeautifulSoup(open(html_filename),"html.parser")
        if len(soup.findAll(text='No errors to report!')) == 1:
            audit.at[row, "NoErrorsToReport"] = "True"
        else:
            audit.at[row, "NoErrorsToReport"] = "False"
       

    # no html file generated
    else:
        audit.at[row, 'HasHTML'] = "False"
        audit.at[row, "NoErrorsToReport"] = "False"

    # grab the last line of the error file

    #e_files = []
    #subject = audit.iloc[row]["SubjectID"]
    
    if rerun == True: #and subject in rerun_subs: 
        #print(subject + " is a rerun")
        
        # CASE WHERE RERUN .e/.o in same dir as others
        if subject == 'sub-1342487188':
            jobID = '5425206'
        else:
            branch_name = sub_branch_names[subject]
            jobID = branch_name.replace(subject + '-', '')
            print("JOBID", jobID)
        try:
            e_file = sorted(glob.glob('%s/*%s*.e%s'%(rerun_error_dir,subject,jobID)),key=os.path.getmtime)[-1]
        except IndexError:
            e_file = ''
    else:
        #print(subject + " is not a rerun")
        try:
            e_file = sorted(glob.glob('%s/*%s*.e*'%(error_dir,subject)),key=os.path.getmtime)[-1]
        except IndexError:
            e_file = ''
            #print("no .e file")
    #print(e_file)
    #e_files.append(e_file)
    #print(e_file)    
    # Assume none, overwrite if exists
    print("E_FILE", e_file)
    if e_file != '':
        audit.at[row, "HasErrorFile"] = "True"
        audit.at[row, "RuntimeErrorDescription"] = "No Runtime Error"
        audit.at[row, "OSErrorDescription"] = "No OS Error"
        audit.at[row, "CommandErrorDescription"] = "No Command Error"
        audit.at[row, "HadScratchSpace"] = "True"
        audit.at[row, "HadRAMSpace"] = "True"
        audit.at[row, "HadDiskSpace"] = "True"
        audit.at[row, "FinishedSuccessfully"] = "False"
        with open(e_file) as f:
            for line in f:
                # get runtime error if exists
                if "RuntimeError:" in line:
                    audit.at[row, "RuntimeErrorDescription"] = line
                # get OS error if exists
                if "OSError:" in line:
                    audit.at[row, "OSErrorDescription"] = line
                # get command error if exists
                if "CommandError:" in line:
                    audit.at[row, "CommandErrorDescription"] = line
                # check if no space, indicated by 4 print statements we know of
                if "No space left on device" in line or "not enough free space" in line or "fatal: failed to copy file to '/scratch/" in line:
                    audit.at[row, "HadScratchSpace"] = "False"
                if "Cannot allocate memory" in line: 
                    audit.at[row, "HadRAMSpace"] = "False"
                if "[INFO] Finished push of Dataset(/scratch" in line:
                    audit.at[row, "FinishedSuccessfully"] = "True"
                if "Disk quota exceeded" in line:
                    audit.at[row, "HadDiskSpace"] = "False"
    else: 
        audit.at[row, "HasErrorFile"] = "False"
        audit.at[row, "RuntimeErrorDescription"] = ""
        audit.at[row, "OSErrorDescription"] = ""
        audit.at[row, "CommandErrorDescription"] = ""
        audit.at[row, "HadScratchSpace"] = ""
        audit.at[row, "HadRAMSpace"] = ""
        audit.at[row, "FinishedSuccessfully"] = ""
                                                
    # THE REST IS PIPELINE DEPENDENT
    
    if pipeline == "qsiprep":

        # check if bids_dir has dwi data
        #if Path(bids_dir + "/" + audit.iloc[row]["SubjectID"] + "/" + get_ses_name(Path(audit.iloc[row]["Path"])) + "/dwi/").exists():
        for ses_path in Path(bids_dir + "/" + audit.iloc[row]["SubjectID"]).glob("ses-*/"):
            #print(ses_path)
            if Path(str(ses_path) + "/dwi/").exists():
                audit.at[row, 'HasDwiDir'] = "True"

                # checking for missing PhaseEncodingDirection

                #for filepath in Path(bids_dir + "/" + audit.iloc[row]["SubjectID"] + "/" + get_ses_name(Path(audit.iloc[row]["Path"])) + "/dwi/").rglob("*.json"):
                for filepath in Path(str(ses_path)).rglob("dwi/*.json"):
                    #print(filepath)
                    IntendedForMissing = False
                    MissingdPED = False

                    filestr = str(filepath)
                    with open(filestr) as f:
                        data = json.load(f)

                    # Check for PhaseEncodingDirection
                    if filestr.endswith("_dwi.json"):
                        if "PhaseEncodingDirection" not in list(data.keys()):
                            MissingdPED = True
                if MissingdPED == False:
                    audit.at[row, "NoMissingDwiPhaseEncodingDirection"] = "True"
                else:
                    audit.at[row, "NoMissingDwiPhaseEncodingDirection"] = "False"

            else:
                audit.at[row, 'HasDwiDir'] = "False"
                audit.at[row, "NoMissingDwiPhaseEncodingDirection"] = "False"

        # now want to check if fmap directories are present in the bids dir
        # if Path(bids_dir + "/" + audit.iloc[row]["SubjectID"] + "/" + get_ses_name(Path(audit.iloc[row]["Path"])) + "/fmap/").exists():
        for ses_path in Path(bids_dir + "/" + audit.iloc[row]["SubjectID"]).glob("ses-*/"):
            #print(ses_path)
            if Path(str(ses_path) + "/fmap/").exists():
                audit.at[row, "HasFmapDir"] = "True"

                # checking if fmaps have intended fors
                #for filepath in Path(bids_dir + "/" + audit.iloc[row]["SubjectID"] + "/" + get_ses_name(Path(audit.iloc[row]["Path"])) + "/fmap/").rglob("*.json"):
                IntendedForMissing = False
                MissingfPED = False
                for filepath in Path(str(ses_path)).rglob("fmap/*.json"):

                    filestr = str(filepath)
                    with open(filestr) as f:
                        data = json.load(f)

                    # Check for IntendedFor
                    if "IntendedFor" not in list(data.keys()):
                        IntendedForMissing = True
                    # empty IntendedFor case
                    elif len(data["IntendedFor"]) == 0:
                        IntendedForMissing = True

                    # Check for PhaseEncodingDirection
                    if filestr.endswith("_epi.json"):
                        #print(list(data.keys()))
                        if "PhaseEncodingDirection" not in list(data.keys()):
                            MissingfPED = True

                if IntendedForMissing == False:
                    audit.at[row, "AllFmapsHaveIntendedFors"] = "True"
                else:
                    audit.at[row, "AllFmapsHaveIntendedFors"] = "False"

                if MissingfPED == False:
                    audit.at[row, "NoMissingFmapPhaseEncodingDirection"] = "True"
                else:
                    audit.at[row, "NoMissingFmapPhaseEncodingDirection"] = "False"
            else:
                audit.at[row, "HasFmapDir"] = "False"
                audit.at[row, "AllFmapsHaveIntendedFors"] = "False"
                audit.at[row, "NoMissingPhaseEncodingDirection"] = "False"

        # check if qsiprep generated dwi
        #if Path(audit.iloc[row]["Path"] + "/" + get_ses_name(Path(audit.iloc[row]["Path"])) + "/dwi/").exists():
        for ses_path in Path(audit.iloc[row]["Path"]).glob("ses-*/"):
            #print(ses_path)
            if Path(str(ses_path) + "/dwi/").exists():
                audit.at[row, "ProducedPreprocessedDWIs"] = "True"
            else:
                audit.at[row, "ProducedPreprocessedDWIs"] = "False"

        # check if qsiprep generated anat
        if Path(audit.iloc[row]["Path"] + "/anat/").exists():
            audit.at[row, "ProducedPreprocesedANATs"] = "True"
            # now check for .h5 files
            spacial = False
            for filename in Path(audit.iloc[row]["Path"]).glob("anat/*"):
                if str(filename).endswith(".h5"):
                    spacial = True
            if spacial == True:
                audit.at[row, "RanT1wSpatialNormalization"] = "True"
            else:
                audit.at[row, "RanT1wSpatialNormalization"] = "False"
        else:
            audit.at[row, "ProducedPreprocesedANATs"] = "False"
            audit.at[row, "RanT1wSpatialNormalization"] = "False"

    if pipeline == "fmriprep":
        # check if sub in bids_dir but not output_dir
        #for ses_path in Path(bids_dir _ "/" + audit.iloc[row]["SubjectID"]):
        #if Path(output_dir _ "/" + audit.iloc[row]["SubjectID"]).exists():
            #audit.a
        
        # check for bold scans in bids dir and output dir
        for ses_path in Path(bids_dir + "/" + audit.iloc[row]["SubjectID"]).glob("ses-*/"):
            
            if Path(str(ses_path) + "/func/").exists():
                audit.at[row, "HasFuncDir"] = "True"
        
                has_bold = False
                for filepath in Path(str(ses_path)).rglob("func/*"):
                    if "bold" in str(filepath):
                        #print(str(filepath))
                        has_bold = True
                if has_bold == True:
                    audit.at[row, "HasBold"] = "True"
                else:
                    audit.at[row, "HasBold"] = "False"
            else:
                audit.at[row, "HasFuncDir"] = "False"
                audit.at[row, "HasBold"] = "False"

        for ses_path in Path(output_dir + "/" + audit.iloc[row]["SubjectID"]).glob("ses-*/"):
            if Path(str(ses_path) + "/func/").exists():
                audit.at[row, "ProducedFuncDir"] = "True"
                has_surf_bold = False
                has_vol_bold = False
                for filepath in Path(str(ses_path)).rglob("func/*"):
                    if "fsLR_den-91k_bold.dtseries" in str(filepath):
                        #print(str(filepath))
                        has_surf_bold = True
                    if "MNI152NLin2009cAsym_desc-preproc_bold" in str(filepath):
                        has_vol_bold = True 
                        #print(str(filepath))
                if has_surf_bold == True:
                    audit.at[row, "RanSurfBold"] = "True"
                else:
                    audit.at[row, "RanSurfBold"] = "False"
                
                if has_vol_bold == True:
                    audit.at[row, "RanVolBold"] = "True"
                else:
                    audit.at[row, "RanVolBold"] = "False"

            else:
                audit.at[row, "ProducedFuncDir"] = "False"
                audit.at[row, "RanSurfBold"] = "False"
                audit.at[row, "RanVolBOld"] = "False"

# REMOVE PATH
audit = audit.drop(["Path"], axis=1)

# write output to a csv
audit.to_csv(sys.argv[5])
print("Saved audit csv")
# audit.to_csv("/Users/scovitz/abcd/audit.csv")

# chekcout back to master (commented out because this adds runtime and isn't necessary) 
# BUT MAKE IT BLOCKING
#msg = subprocess.call(["git", "checkout", "master"], stdout=subprocess.PIPE, cwd=output_dir)
#subprocess.Popen(["git", "checkout", "master"], cwd=output_dir)

# checkout to master 
msg = subprocess.call(["git", "checkout", "master"], stdout=subprocess.PIPE, cwd=output_dir)
