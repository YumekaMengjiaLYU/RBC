#!/usr/bin/env python
import os
import glob
import pandas as pd
import numpy as np


subzips = glob.glob('*zip*')

for subzip in subzips:
	sid = subzip.split('colornest')[1].split('_')[0]
	os.system('datalad get {0}'.format(subzip))
	os.system('datalad unlock {0}'.format(subzip))
	os.system('git annex dead here')

for subzip in subzips:
	sid = subzip.split('colornest')[1].split('_')[0]

	cmd = 'unzip -p {1} "xcp_abcd/sub-colornest{0}/ses-1/func/sub-colornest{0}_ses-1_task-rest_run-1_space-MNI152NLin2009cAsym_atlas-Schaefer417_desc-timeseries_bold.tsv" > matrices/fc_run1_{0}.tsv'.format(sid,subzip)
	os.system(cmd)
	cmd = 'unzip -p {1} "xcp_abcd/sub-colornest{0}/ses-1/func/sub-colornest{0}_ses-1_task-rest_run-2_space-MNI152NLin2009cAsym_atlas-Schaefer417_desc-timeseries_bold.tsv" > matrices/fc_run2_{0}.tsv'.format(sid,subzip)
	os.system(cmd)
