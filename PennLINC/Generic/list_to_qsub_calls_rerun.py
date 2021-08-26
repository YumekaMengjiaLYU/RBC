#!/usr/bin/env python

import subprocess
import sys
import os
from pathlib import Path
import glob 
import pandas as pd

analysis_dir = sys.argv[1]
rerun_txt = sys.argv[2]
if Path(analysis_dir).exists():
    rerun_df = pd.read_csv(rerun_txt, header=None)
    l_rerun_subs = rerun_df[0].tolist()

    # NOW truncate qsub_calls.sh!
    df = pd.read_csv(analysis_dir + '/code/qsub_calls.sh')
    for row in range(len(df)):
        if df.loc[row, '#!/bin/bash'].split(' ')[-2] not in l_rerun_subs:
            # remove that row 
            df.drop([row], inplace = True)
    
    # write out qsub_calls_rerun.sh
    df = df.reset_index()
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

