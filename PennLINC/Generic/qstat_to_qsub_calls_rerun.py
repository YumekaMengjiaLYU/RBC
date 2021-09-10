#!/usr/bin/env python

import subprocess
import sys
import os
from pathlib import Path
import glob 
import pandas as pd

analysis_dir = sys.argv[1]

qstat = subprocess.check_output(['qstat'],shell=True).decode().split('/bin/python')[0]
lines = qstat.split('\n')

# get jobids from qstat
job_ids = []
for i in range(len(lines)):
    if 1 < i < len(lines)-1:
        jid = lines[i].split(' ')[0]
        job_ids.append(jid)
#print("NUM JOB IDS", len(job_ids))

# get subids from logs dir
sub_ids = []
if Path(analysis_dir).exists():
    print("ANALYSIS")
    sp = subprocess.Popen(["ls"], stdout=subprocess.PIPE,
            cwd=analysis_dir + '/logs')
    logs = sp.stdout.readlines()
    # print(logs[0])
    jobs_to_delete = []
    for log in logs:
        for jid in job_ids:
            if jid in str(log) and '.o' in str(log):
                subid = 'sub-' + str(log).split('.o')[0].split('sub-')[1]
                sub_ids.append(subid)
                jobs_to_delete.append(jid)
    print("NUM SUBIDS", len(sub_ids))
    
    # NOW truncate qsub_calls.sh!
    df = pd.read_csv(analysis_dir + '/code/qsub_calls.sh')
    for row in range(len(df)):
        if df.loc[row, '#!/bin/bash'].split(' ')[-2] not in sub_ids:
            # remove that row 
            df.drop([row], inplace = True)
        
    df = df.reset_index()
    
    # if the remaining number of qsub calls is correct
    print(len(df))
    print(len(jobs_to_delete))
    if len(df) == len(jobs_to_delete):
        for jid in job_ids:
            # delete job id
            print("YAY GOOD") 
            #subprocess.run(['qdel', '-j', jid])
    
    # write out qsub_calls_rerun.sh
    l_cmd = []
    for row in range(len(df)):
        l_cmd.append(df.loc[row, '#!/bin/bash'])
    full_cmd = "\n".join(l_cmd)
    fileObject = open(analysis_dir + "/code/qsub_calls_rerun.sh","w")
    fileObject.write("#!/bin/bash\n")
    fileObject.write(full_cmd)
    # Close the file
    fileObject.close()
else:
    print("PLEASE ENTER A VALID ANALYSIS DIR")

