

## Get those DWI:

dataout='/cbica/projects/RBC/CPACTesting/Pipeline_Timing/Missint_DWI'

while IFS=, read -r sub site rest; do
    echo $sub $site

    awspatth='s3://fcp-indi/data/Projects/HBN/MRI/'$site'/'$sub'/dwi'

    aws s3 sync $awspatth $dataout'/data_orig/'$site'/'$sub'/dwi' --exclude "*TRACEW*"
done < $dataout'/curation_dwi_mismatch.csv'






## check some names with run-
# rename and remove



## 
run='_run-02'
orig=data_orig/Site-CBIC/sub-NDARHN078CDT/dwi/sub-NDARHN078CDT_acq-64dir_run-02_dwi.nii.gz

run='_run-03'
orig=data_orig/Site-CBIC/sub-NDARBM764KG0/dwi/sub-NDARBM764KG0_acq-64dir_run-03_dwi.nii.gz

run='_run-02'
orig='data_orig/Site-CBIC/sub-NDARXW045HPY/dwi/sub-NDARXW045HPY_acq-64dir_run-02_dwi.nii.gz'

run='_run-02'
orig='data_orig/Site-CBIC/sub-NDARRA981BCM/dwi/sub-NDARRA981BCM_acq-64dir_run-02_dwi.nii.gz'

run='_run-02'
orig='data_orig/Site-CBIC/sub-NDARUP441BKK/dwi/sub-NDARUP441BKK_acq-64dir_run-02_dwi.nii.gz'

run='_run-03'
orig='data_orig/Site-CBIC/sub-NDARHN482HPM/dwi/sub-NDARHN482HPM_acq-64dir_run-03_dwi.nii.gz'

run='_run-02'
orig='data_orig/Site-CBIC/sub-NDARXX939FFN/dwi/sub-NDARXX939FFN_acq-64dir_run-02_dwi.nii.gz'

run='_run-02'
orig='data_orig/Site-CBIC/sub-NDARHN078CDT/dwi/sub-NDARHN078CDT_acq-64dir_run-02_dwi.nii.gz'



x=$orig
mv $x ${x/$run}

x=${orig/.nii.gz/.json}
mv $x ${x/$run}

x=${orig/.nii.gz/.bvec}
mv $x ${x/$run}

x=${orig/.nii.gz/.bval}
mv $x ${x/$run}

rm -r $(find $(dirname $orig) -iname '*run*')


rm -r data_orig/Site-RU/sub-NDARMU589LP6




## re-structure them:
# /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARMB216LA6/ses-HBNsiteCBIC/dwi/sub-NDARMB216LA6_ses-HBNsiteCBIC_acq-64dir_dwi.nii.gz@
datain='/cbica/projects/RBC/CPACTesting/Pipeline_Timing/Missint_DWI/data_orig'
dataout='/cbica/projects/RBC/CPACTesting/Pipeline_Timing/Missint_DWI/data_BIDS'

for site in $(ls $datain);do
    echo $site
    site1=${site/Site-/}
    ses='HBNsite'${site1/"/"/}
    for sub in $(ls $datain'/'$site);do
        sub=${sub/"/"/}
        echo $sub
        for i in $(find $datain'/'$site''$sub -type f);do
            echo $i 
            i_file=$(basename $i)
            sub_ses=$sub'_ses-'$ses
            i_new=$dataout'/'$sub'/ses-'$ses'/dwi/'${i_file/$sub/$sub_ses}
            echo $i_new
            mkdir -p $(dirname $i_new)
            ln -s $i $i_new
        done
    done
done



### putting htem in to the HBN folder:
datain='/cbica/projects/RBC/CPACTesting/Pipeline_Timing/Missint_DWI/data_BIDS'
dataout='/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN'
for sub in $(ls $datain);do
    if [[ -d $dataout'/'$sub ]];then
        for file in $(find $datain'/'$sub -type l);do
            echo $file
            file_new=${file/$datain/$dataout}
            echo $file_new
            mkdir -p $(dirname $file_new)
            cp -L $file $file_new
        done
        echo $sub
    fi
done

# check if they have fmap
datain='/cbica/projects/RBC/CPACTesting/Pipeline_Timing/Missint_DWI/data_BIDS'
dataout='/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN'
for sub in $(ls $datain);do
    if [[ -d $dataout'/'$sub ]];then
        find $dataout'/'$sub -path '*ses-HBNsiteSI/fmap*' -iname '*nii.gz*'
    fi
done


### Notes:
# RU has both fmri and dwi fmap,
# CBIC does not had DWI fmap need to add. also add the IntendedFor.
# SI has dWI fmap, need to add the IntendedFor in.


### get fmaps for dwi from CBIC :
dataout='/cbica/projects/RBC/CPACTesting/Pipeline_Timing/Missint_DWI'
while IFS=, read -r sub site rest; do
    if [[ $site != *"CBIC"* ]];then continue;fi
    echo $sub $site
    awspatth='s3://fcp-indi/data/Projects/HBN/MRI/'$site'/'$sub'/fmap'
    aws s3 sync $awspatth $dataout'/data_orig/'$site'/'$sub'/fmap' --exclude "*acq-fMRI*"
done < $dataout'/curation_dwi_mismatch.csv'

# restructure
datain='/cbica/projects/RBC/CPACTesting/Pipeline_Timing/Missint_DWI/data_orig'
dataout='/cbica/projects/RBC/CPACTesting/Pipeline_Timing/Missint_DWI/data_BIDS'

for site in $(ls $datain);do
    echo $site
    site1=${site/Site-/}
    ses='HBNsite'${site1/"/"/}
    for sub in $(ls $datain'/'$site);do
        sub=${sub/"/"/}
        echo $sub
        for i in $(find $datain'/'$site''$sub -type f -path '*fmap*' );do
            echo $i 
            i_file=$(basename $i)
            sub_ses=$sub'_ses-'$ses
            i_new=$dataout'/'$sub'/ses-'$ses'/fmap/'${i_file/$sub/$sub_ses}
            echo $i_new
            mkdir -p $(dirname $i_new)
            ln -s $i $i_new
        done
    done
done

# firstt change the name of files, switch the order of dir- and acq-

for i in $(find /cbica/projects/RBC/CPACTesting/Pipeline_Timing/Missint_DWI/data_BIDS -path "*fmap*" -type l);do
    echo -----
    echo $i
    i_new=${i/dir-PA_acq-dwi/acq-dwi_dir-PA}
    i_new=${i_new/dir-AP_acq-dwi/acq-dwi_dir-AP}
    i_new=${i_new/dir-PA_acq-fMRI/acq-fMRI_dir-PA}
    i_new=${i_new/dir-AP_acq-fMRI/acq-fMRI_dir-AP}
    echo $i_new
    mv $i $i_new
done

### putting htem in to the HBN folder:
cc=0
datain='/cbica/projects/RBC/CPACTesting/Pipeline_Timing/Missint_DWI/data_BIDS'
dataout='/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN'
for sub in $(ls $datain);do
    if [[ -d $dataout'/'$sub ]];then
        for file in $(find $datain'/'$sub -type l -path '*fmap*');do
            #echo $file
            file_new=${file/$datain/$dataout}
            #echo $file_new
            if [[ ! -f $file_new ]];then
                echo $file_new
                cc=$((cc+1))
                mkdir -p $(dirname $file_new)
                cp -L $file $file_new
            fi
        done
        #echo $sub
    fi
done


######### python scripts to put indented for into fmap json for dwi images. 
import json
import os
import numpy as np
subfolder = '/cbica/projects/RBC/CPACTesting/Pipeline_Timing/Missint_DWI/data_BIDS'
dataout = '/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN'

for sub in os.listdir(subfolder):
    print(sub)
    indentedfor_list=[]
    for ses in os.listdir(dataout + '/' + sub ):
        if os.path.isdir(dataout + '/' + sub + '/' + ses + '/dwi'):
            for file in os.listdir(dataout + '/' + sub + '/' + ses + '/dwi'):
                if 'nii.gz' in file:
                    print(file)
                    indentedfor  = ses + '/dwi/' + file
                    indentedfor_list.append(indentedfor)
                    print(indentedfor_list)
        ### fmap
        if os.path.isdir(dataout + '/' + sub + '/' + ses + '/fmap'):
            for file in os.listdir(dataout + '/' + sub + '/' + ses + '/fmap'):
                if 'json' in file and 'acq-dwi' in file:
                    print(file)
                    file_long=dataout + '/' + sub + '/' + ses + '/fmap/' + file
                    with open(file_long) as f:
                        data = json.load(f)
                    data['IntendedFor']=indentedfor_list
                    with open(file_long, 'w') as json_file:
                        json.dump(data, json_file,indent=4)






#### python to add 

#    "IntendedFor": [
#        "ses-HBNsiteCBIC/func/sub-NDARHL822EJK_ses-HBNsiteCBIC_task-rest_run-2_bold.nii.gz",
#        "ses-HBNsiteCBIC/func/sub-NDARHL822EJK_ses-HBNsiteCBIC_task-rest_run-1_bold.nii.gz"
#    ],


cc=0;
for i in $(ls);do 
for ses in $(ls $i);do 
xx=${i}${ses}'/dwi';
if [[ ! -d $xx ]];then
cc=$((cc+1));
echo $i$ses

yy=$(aws s3 ls 's3://fcp-indi/data/Projects/HBN/MRI/Site-'${ses/'ses-HBNsite'/}$i'dwi')
echo $yy
fi;
done;
done
