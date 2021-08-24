import pandas as pd
import subprocess
import zipfile
import numpy as np
import sys
import os
import shutil
import matplotlib
import matplotlib.pyplot as plt
import nilearn.image as nim
import nilearn.plotting as nip

#sys.argv[0] = subid
subid = sys.argv[1]
# input dir
input_zip_dir = sys.argv[2]

# temp dir

unzip_temp_dir = sys.argv[3]
#unzip_fs_dir = sys.argv[4]
##input_zip_dir = sys.argv[3]

# output dir
png_path = sys.argv[4]

#unzip_fs_dir = sys.argv[5]
audit_path = sys.argv[5]


columns = ['SubjectID', 'AverageEulerNumber', 'LeftEulerNumber', 'RightEulerNumber', 'LeftDefectIndex', 'RightDefectIndex',
'LeftNumHoles', 'RightNumHoles', 'LeftMeanCorticalThickness', 'RightMeanCorticalThickness', 'LeftPialSurfaceArea',
'RightPialSurfaceArea', 'LeftCorticalGrayMatterVolume', 'RightCorticalGrayMatterVolume',
'TotalCorticalGrayMatterVolume', 'TotalSubcorticalGrayMatterVolume']

fs_audit = pd.DataFrame(np.nan, index=range(0,1), columns=columns, dtype="string")


#subid = 'sub-192413932'

fs_audit['SubjectID'] = subid

with zipfile.ZipFile(input_zip_dir + '/' + subid +
'_freesurfer-20.2.3.zip', 'r') as zip_ref:
    zip_ref.extractall(unzip_temp_dir)

l_euler_path = unzip_temp_dir + '/freesurfer/' + subid + '/surf/lh.orig.nofix'
r_euler_path = unzip_temp_dir + '/freesurfer/' + subid + '/surf/rh.orig.nofix'

subprocess.run(["mris_euler_number", "-o", unzip_temp_dir + "/l_euler.txt", l_euler_path])
subprocess.run(["mris_euler_number", "-o", unzip_temp_dir + "/r_euler.txt", r_euler_path])
l_euler = open(unzip_temp_dir + "/l_euler.txt","r")

l_num_holes = int(l_euler.readlines()[0].split(' ')[3].strip('\n'))
fs_audit['LeftNumHoles'] = l_num_holes
l_euler_number = abs(2 - 2*l_num_holes)
fs_audit['LeftEulerNumber'] = l_euler_number
l_defect_index = 2*l_num_holes
fs_audit['LeftDefectIndex'] = l_defect_index

r_euler = open(unzip_temp_dir+ "/r_euler.txt","r")
r_num_holes = int(r_euler.readlines()[0].split(' ')[3].strip('\n'))
fs_audit['RightNumHoles'] = r_num_holes
r_euler_number = abs(2 - 2*r_num_holes)
fs_audit['RightEulerNumber'] = r_euler_number
r_defect_index = 2*r_num_holes
fs_audit['RightDefectIndex'] = r_defect_index
fs_audit['AverageEulerNumber'] = abs(float(l_euler_number + r_euler_number)/2.0)

l_mean_cort_thickness = ''
cort_vol = ''
l_desikan = open(unzip_temp_dir + "/freesurfer/" + subid + "/stats/lh.aparc.DKTatlas.stats", "r")
l_cntr = 0
l_table_start_index = 0
for line in l_desikan.readlines():
    l_cntr += 1
    if l_table_start_index > 0:
        region = line.split()[0]
        surf_area = line.split()[2]
        gray_vol = line.split()[3]
        thick_avg = line.split()[4]
        fs_audit['LeftSurfArea_' + region] = surf_area
        fs_audit['LeftGrayVol_' + region] = gray_vol
        fs_audit['LeftThickAvg_' + region] = thick_avg
    if "MeanThickness" in line:
        l_mean_cort_thickness = float(line.split(' ')[-2].strip(','))
    if "CortexVol" in line:
        cort_vol = float(line.split(' ')[-2].strip(','))
    # get region table into a pandas df
    if "ColHeaders" in line:
        l_table_start_index = l_cntr


fs_audit['LeftMeanCorticalThickness'] = l_mean_cort_thickness
fs_audit['TotalCorticalGrayMatterVolume'] = cort_vol

r_desikan = open(unzip_temp_dir + "/freesurfer/" + subid + "/stats/rh.aparc.DKTatlas.stats", "r")
r_table_start_index = 0
r_cntr = 0
for line in r_desikan.readlines():
    r_cntr +=1
    if r_table_start_index > 0:
        region = line.split()[0]
        surf_area = line.split()[2]
        gray_vol = line.split()[3]
        thick_avg = line.split()[4]
        fs_audit['RightSurfArea_' + region] = surf_area
        fs_audit['RightGrayVol_' + region] = gray_vol
        fs_audit['RightThickAvg_' + region] = thick_avg
    if "MeanThickness" in line:
        r_mean_cort_thickness = float(line.split(' ')[-2].strip(','))
    if "ColHeaders" in line:
        r_table_start_index = r_cntr

fs_audit['RightMeanCorticalThickness'] = r_mean_cort_thickness

surf_area = ''
l_pial = open(unzip_temp_dir + "/freesurfer/" + subid + "/stats/lh.aparc.pial.stats", "r")
r_pial = open(unzip_temp_dir + "/freesurfer/" + subid + "/stats/rh.aparc.pial.stats", "r")

for line in l_pial:
    if "PialSurfArea" in line:
        l_surf_area = float(line.split(' ')[-2].strip(','))
for line in r_pial:
    if "PialSurfArea" in line:
        r_surf_area = float(line.split(' ')[-2].strip(','))

fs_audit["LeftPialSurfaceArea"] = l_surf_area
fs_audit["RightPialSurfaceArea"] = r_surf_area

l_cort_vol = ''
r_cort_vol = ''
subcort_vol = ''
aseg = open(unzip_temp_dir + "/freesurfer/" + subid + "/stats/aseg.stats", "r")
for line in aseg:
    if "SubCortGrayVol" in line:
        subcort_vol = float(line.split(' ')[-2].strip(','))
    if "lhCortexVol" in line:
        l_cort_vol = float(line.split(' ')[-2].strip(','))
    if "rhCortexVol" in line:
        r_cort_vol = float(line.split(' ')[-2].strip(','))
fs_audit["LeftCorticalGrayMatterVolume"] = l_cort_vol
fs_audit["RightCorticalGrayMatterVolume"] = r_cort_vol

fs_audit["TotalSubcorticalGrayMatterVolume"] = subcort_vol

# for gray matter surface area, cort vol, just add l + r
# for mean cort thickness, just average l  and r
# KEEP ALL SEPARATE

preordered = columns
non_preordered = set(fs_audit.columns) - set(preordered)

r_thick_avg = []
l_thick_avg = []
r_gray_vol = []
l_gray_vol = []
r_surf_area = []
l_surf_area = []
for val in non_preordered:
    if "RightThickAvg" in val:
        r_thick_avg.append(val)
    if "RightGrayVol" in val:
        r_gray_vol.append(val)
    if "RightSurfArea" in val:
        r_surf_area.append(val)
    if "LeftThickAvg" in val:
        l_thick_avg.append(val)
    if "LeftGrayVol" in val:
        l_gray_vol.append(val)
    if "LeftSurfArea" in val:
        l_surf_area.append(val)


new_non_preordered = sorted(r_gray_vol) + sorted(l_gray_vol) + sorted(r_surf_area) + \
                     sorted(l_surf_area) + sorted(r_thick_avg) + sorted(l_thick_avg)

new_order = preordered + new_non_preordered
fs_audit = fs_audit.reindex(columns=new_order)

#fs_audit.to_csv('/cbica/projects/RBC/Curation/RBC/PennLINC/PNC_BIDS_Fix/PNC_CSVs/00_Ordered/mount/fs_audit.csv', index=False)

fs_audit.to_csv(audit_path)

path_t1w = 'fmriprep/'+ subid + '/ses-PNC1/anat/%s_ses-PNC1_acq-refaced_desc-preproc_T1w.nii.gz'%(subid) 
basename = '%s_ses-PNC1_acq-refaced_desc-preproc_T1w.nii.gz'%(subid)

path_unzip_t1w = unzip_temp_dir +'/%s_ses-PNC1_acq-refaced_desc-preproc_T1w.nii.gz'%(subid) 

with zipfile.ZipFile(input_zip_dir + '/' + subid + '_fmriprep-20.2.3.zip', 'r') as zip_ref_fmri:
    with zip_ref_fmri.open(path_t1w) as zf, open(os.path.join(unzip_temp_dir,os.path.basename(basename)),'wb') as f:
        #listOfFileNames = zip_ref_fmri.namelist()
        shutil.copyfileobj(zf,f)

    #zip_ref_fmri.extract(member=path_t1w)

# test one single subject
# path_unzip_t1w = unzip_temp_dir + '/fmriprep/' + subid + '/ses-PNC1/anat/sub-192413932_ses-PNC1_acq-refaced_desc-preproc_T1w.nii.gz'
image_t1w = nim.load_img(path_unzip_t1w)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15,15))
nip.plot_img(image_t1w, axes=ax, black_bg=True, 
             title="%s-%d"%(subid,
                 fs_audit['AverageEulerNumber']),cmap="gray",draw_cross=False)
fig.savefig(png_path)

