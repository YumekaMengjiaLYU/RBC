#/bin/bash

# This will deface other image types (T2, MTIs) based the good defaced T1 from a same subject.


#usuage: deface_other_image.sh T1.nii.gz, T1_defaced.nii.gz T2.nii.gz

#goodhead='/data2/HBNcore/CMI_HBN_Data/MRI/RU/Release/R4_20171201_20180531/data/sub-5159583/anat/sub-5159583_acq-HCP_T1w_defaced_blocked.nii.gz'

#gooddeface='/data2/HBNcore/CMI_HBN_Data/MRI/RU/Release/R4_20171201_20180531/data/sub-5159583/anat/sub-5159583_acq-HCP_T1w_defaced_blocked.nii.gz'

#target='/data2/HBNcore/CMI_HBN_Data/MRI/RU/Release/R4_20171201_20180531/data/sub-5159583/anat/sub-5159583_acq-HCP_T2w.nii.gz'


gooddeface=$1
target=$2
goodhead=$gooddeface



if [[ ! -f ${target/.nii.gz/_blocked.nii.gz} ]];then

working_dir=$(dirname $goodhead)'/temp_deface_'$RANDOM
mkdir -p $working_dir

#if [[ -f $(dirname $goodhead)'/brain_mask.nii.gz' ]];then
#    mv $(dirname $goodhead)'/brain_mask.nii.gz' $working_dir'/good_brain_mask.nii.gz'
#fi

# if brain mask not exist
if [[ ! -f $working_dir'/good_brain_mask.nii.gz' ]];then
    3dSkullStrip -input $goodhead -mask_vol -prefix $working_dir'/good_brain_mask.nii.gz'
    fslmaths $working_dir'/good_brain_mask.nii.gz' -kernel sphere 3 -dilM -bin $working_dir'/good_brain_mask.nii.gz'
fi



# make defaced mask
fslmaths $gooddeface -bin $working_dir'/gooddeface_mask.nii.gz'

flirt -in $target -ref $goodhead -dof 6 -omat $working_dir'/target2goodhead.mat'

# inverset the mat
convert_xfm -omat $working_dir'/goodhead2target.mat' -inverse $working_dir'/target2goodhead.mat'

# apply the inverst mat to the deface mask
flirt -in $working_dir'/gooddeface_mask.nii.gz' -ref $target -applyxfm -init $working_dir'/goodhead2target.mat' -o $working_dir'/target_deface_mask.nii.gz'

# apply the inverst mat to the T1 brain mask to generate the target brain mask
flirt -in $working_dir'/good_brain_mask.nii.gz' -ref $target -applyxfm -init $working_dir'/goodhead2target.mat' -o $working_dir'/target_brain_mask.nii.gz'

# combine two masks (deface mask and brain mask)
fslmaths $working_dir'/target_deface_mask.nii.gz' -add $working_dir'/target_brain_mask.nii.gz' -bin $working_dir'/target_deface_mask_final.nii.gz'

fslmaths $target -mul $working_dir'/target_deface_mask_final.nii.gz' ${target/.nii.gz/_blocked.nii.gz}

rm -r $working_dir

else
echo 'Already Defaced'

fi
