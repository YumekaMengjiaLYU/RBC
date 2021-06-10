#!/usr/bin/env python
import os
import glob
import pandas as pd
import numpy as np
import nibabel as nib

os.makedirs('all_matrices',exist_ok=True)
subzips = glob.glob('concat_ds/*zip*')

for subzip in subzips:
	sid = subzip.split('colornest')[1].split('_')[0]
	cmd = 'unzip {0} -d all_matrices/'.format(subzip)
	os.system(cmd)



df = pd.DataFrame()
for csv in glob.glob('*qc_bold.tsv'):
	df = df.append(pd.read_csv(csv),ignore_index=True)

df = df.sort_values('sub')

parcels = ['Gordon','Glasser']

for parcel in parcels:
	matrices = []
	for matrix in df.iterrows():
		matrix = dict(matrix[1])
		if type(matrix['acq']) == str:
			matrices.append(nib.load('all_matrices/matrices/sub-{0}_ses-{1}_task-{2}_acq-{5}_run-{3}_space-fsLR_atlas-{4}_den-91k_bold.pconn.nii'.format(matrix['sub'],matrix['ses'],matrix['task'],matrix['run'],parcels,matrix['acq'])).get_fdata())
			continue
		if np.isnan(matrix['acq']):
			matrices.append(nib.load('all_matrices/matrices/sub-{0}_ses-{1}_task-{2}_run-{3}_space-fsLR_atlas-{4}_den-91k_bold.pconn.nii'.format(matrix['sub'],matrix['ses'],matrix['task'],matrix['run'],parcels)).get_fdata())
			continue
		1/0 #should never get here!!
	matrices = np.array(matrices)
	assert matrices.shape[0] == df.shape[0]
	np.save('{0}_group_matrix.npy'.format(parcel),matrices)

df.to_csv('group_fc.csv')
os.system('zip group_matrices.zip *group*')
