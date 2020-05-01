# Deface using mri_deface and correct any face remaining and brain cut

## 1. Auto deface using this tool:
https://surfer.nmr.mgh.harvard.edu/fswiki/mri_deface
 
However, this fails about 40%, so some corrections are needed.
 
### Also I have noticed that the new version fo the mri_deface does not work, if that is the case, use the old version from this repo. 
 
## 2. Run the correct_AutoDeface.sh to fix the auto deface. It can be run as following:
correct_AutoDeface.sh T1.nii.gz T1_defaced.nii.gz
 
T1_defaced.nii.gz is the defaced image from step one, while the T1.nii.gz is the original T1 image.
 
The bash scripts will call a python function, the path of the python script in the bash script need to be changed.
 
Let me know if you have any problems.