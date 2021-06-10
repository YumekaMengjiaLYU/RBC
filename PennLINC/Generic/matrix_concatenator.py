#!/usr/bin/env python
import os
import glob
import pandas as pd
import numpy as np
import nibabel as nib

os.makedirs('concat_ds/all_matrices',exist_ok=True)
subzips = glob.glob('concat_ds/*zip*')

for subzip in subzips:
	sid = subzip.split('colornest')[1].split('_')[0]
	cmd = 'unzip {0} -d concat_ds/all_matrices/'.format(subzip)
	os.system(cmd)



df = pd.DataFrame()
for csv in glob.glob('concat_ds/all_matrices/matrices/*qc_bold.tsv'):
	df = df.append(pd.read_csv(csv),ignore_index=True)

df = df.sort_values('sub',axis=0)

parcels = ['Gordon','Glasser']

for parcel in parcels:
	matrices = []
	for matrix in df.iterrows():
		matrix = dict(matrix[1])
		if type(matrix['acq']) == str:
			matrices.append(nib.load('concat_ds/all_matrices/matrices/sub-{0}_ses-{1}_task-{2}_acq-{5}_run-{3}_space-fsLR_atlas-{4}_den-91k_bold.pconn.nii'.format(matrix['sub'],matrix['ses'],matrix['task'],matrix['run'],parcel,matrix['acq'])).get_fdata())
			continue
		if np.isnan(matrix['acq']):
			matrices.append(nib.load('concat_ds/all_matrices/matrices/sub-{0}_ses-{1}_task-{2}_run-{3}_space-fsLR_atlas-{4}_den-91k_bold.pconn.nii'.format(matrix['sub'],matrix['ses'],matrix['task'],matrix['run'],parcel)).get_fdata())
			continue
		1/0 #should never get here!!
	matrices = np.array(matrices)
	assert matrices.shape[0] == df.shape[0]
	np.save('concat_ds/{0}_group_matrix.npy'.format(parcel),matrices)


for parcel in parcels:
	matrices = []
	for matrix in df.iterrows():
		matrix = dict(matrix[1])
		if type(matrix['acq']) == str:
			matrices.append(nib.load('concat_ds/all_matrices/matrices/sub-{0}_ses-{1}_task-{2}_acq-{5}_run-{3}_space-fsLR_atlas-{4}_den-91k_bold.pconn.nii'.format(matrix['sub'],matrix['ses'],matrix['task'],matrix['run'],parcel,matrix['acq'])).get_fdata())
			continue
		if np.isnan(matrix['acq']):
			matrices.append(nib.load('concat_ds/all_matrices/matrices/sub-{0}_ses-{1}_task-{2}_run-{3}_space-fsLR_atlas-{4}_den-91k_bold.pconn.nii'.format(matrix['sub'],matrix['ses'],matrix['task'],matrix['run'],parcel)).get_fdata())
			continue
		1/0 #should never get here!!
	matrices = np.array(matrices)
	assert matrices.shape[0] == df.shape[0]
	np.save('concat_ds/{0}_group_matrix.npy'.format(parcel),matrices)


df.to_csv('concat_ds/group_fc.csv',index=False)
os.system('zip group_matrices.zip concat_ds/*group*')
