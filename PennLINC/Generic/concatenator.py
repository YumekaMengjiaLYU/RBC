#!/usr/bin/env python

# concatenator for audit 
import pandas as pd 
from pathlib import Path 
import numpy as np 
import subprocess
import os
import sys

csv_dir = sys.argv[1]

#columns = ["SubjectID",  "HasOutput", "HasHTML", "NoErrorsToReport", "HasFuncDir", "HasBold", "ProducedFuncDir", "RanSurfBold", "RanVolBold", "HasErrorFile", "RuntimeErrorDescription", "OSErrorDescription", "CommandErrorDescription", "HadScratchSpace", "HadRAMSpace", "HadDiskSpace", "FinishedSuccessfully"]

#df = pd.DataFrame(np.nan, index=range(0,1), columns=columns, dtype="string")

#concatenated_dataframes = pd.concat([dataframe1, dataframe2], axis=1)
cntr = 0
for csv_path in Path(csv_dir).rglob('*.csv'):
    #subprocess.run(['datalad', 'get', csv_path])
    sub_df = pd.read_csv(str(csv_path))
    if cntr == 0: 
        df = sub_df
    else:
        df = pd.concat([df, sub_df], axis=1)
    cntr += 1
#final = df.drop('Unnamed: 0', axis=1)
df.to_csv(sys.argv[2], index=False)
                    
# THEN RUN THIS THROUGH THE SUMMARY REPORT SCRIPTS! 
