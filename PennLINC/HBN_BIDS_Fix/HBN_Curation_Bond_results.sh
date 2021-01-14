## Anatomical T1.

# acquisition-HCP_datatype-anat_run-1_suffix-T1w  
kg='acquisition-HCP_datatype-anat_run-1_suffix-T1w'
while IFS=, read -r keygroup parametergroup filepath
do
    if [[ $keygroup == "$kg" ]];then
    	echo $filepath
    fi
done < HBN_keys_params_simple.csv


datain='/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN'
for sub in $(ls $datain);do
	if [[ $(ls $datain'/'$sub) != "ses-HBNsiteCBIC/" ]];then continue;fi
    #echo $sub
    #find $datain'/'$sub   -iname '*HBNsiteSI*' -path '*anat*' -iname '*nii.gz*' -iname '*run*'
    #find $datain'/'$sub   -iname '*HBNsiteCBIC*' -path '*anat*' -iname '*nii.gz*' -iname '*run-*'
    x1=$(find $datain'/'$sub   -iname '*HBNsiteCBIC*' -path '*anat*' -iname '*nii.gz*' -iname '*run-*' -iname '*VNav*' ! -iname '*VNavNorm*' | wc -l)
    x2=$(find $datain'/'$sub   -iname '*HBNsiteCBIC*' -path '*anat*' -iname '*nii.gz*' -iname '*run-*'  -iname '*VNavNorm*' | wc -l)
    if [[ $x2 == 0 ]] && [[ $x1 != 0 ]];then
    	echo $datain'/'$sub
    fi

done


######### need to restore this accidentally deleted file
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARYR150UDP/ses-HBNsiteRU/func/sub-NDARYR150UDP_ses-HBNsiteRU_task-rest_bold.nii.gz



## 
cd /cbica/projects/RBC/CPACTesting/Pipeline_Timing/HBN_Curation

################ func DM and TP with run-0*, remove extra and only keep 1, usually the last one. 

# 474,475
for run in 4 3 2 1;do
run_type='_run-0'$run
kg='datatype-func_run-'$run'_suffix-bold_task-movieDM'
while IFS=, read -r keygroup parametergroup filepath ooo;
do
    if [[ $keygroup == "$kg" ]];then
        file=`echo $filepath | sed 's/\\r//g'`
        ## remove runs, if not existing, then change the current to to normal name without run, if existing, then delete them.
        file_normal=${file/$run_type/}
        echo $file
        echo $file_normal
        if [[ ! -f $file_normal ]];then
            mv $file $file_normal
            mv ${file/.nii.gz/.json} ${file_normal/.nii.gz/.json}
        else
            rm $file
            rm ${file/.nii.gz/.json}
        fi
    fi
done < HBN_keys_params_simple.csv
done

for run in 4 3 2 1;do
run_type='_run-0'$run
kg='datatype-func_run-'$run'_suffix-bold_task-movieTP'
while IFS=, read -r keygroup parametergroup filepath ooo;
do
    if [[ $keygroup == "$kg" ]];then
        file=`echo $filepath | sed 's/\\r//g'`
        ## remove runs, if not existing, then change the current to to normal name without run, if existing, then delete them.
        file_normal=${file/$run_type/}
        echo $file
        echo $file_normal
        if [[ ! -f $file_normal ]];then
            mv $file $file_normal
            mv ${file/.nii.gz/.json} ${file_normal/.nii.gz/.json}
        else
            rm $file
            rm ${file/.nii.gz/.json}
        fi
    fi
done < HBN_keys_params_simple.csv
done


####### handle the fmap without dir-AP or dir-PA but with run-01 and run-02
# run-01 to dir-AP
# run-02 to dir-PA
datain='/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN'
for sub in $(ls $datain);do
    for ii in $(find $datain'/'$sub -path '*fmap*' -iname '*.json*' -iname '*run-*' ! -iname '*dir*');do
        echo $ii
        ii_new=${ii/_run-02/_dir-PA}
        ii_new=${ii_new/_run-01/_dir-AP}
        mv $ii $ii_new
        mv ${ii/.json/.nii.gz} ${ii_new/.json/.nii.gz}
    done
done


####### handle the multiple fmap
datain='/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN'
for sub in $(ls $datain);do
	for type in acq-dwi_dir-AP acq-dwi_dir-PA acq-fMRI_dir-AP acq-fMRI_dir-PA;do
		checkstatus=0
		for run in 7 6 5 4 3 2 1;do
            for ii in $(find $datain'/'$sub -path '*fmap*' -iname '*.json*' -iname '*run-*' -iname "*$type*" -iname "*_run-0$run*");do
            	if [[ $checkstatus == 0 ]];then
            		checkstatus=1
          	        echo $sub, $type, $run
                    echo $ii
                    ii_new=${ii/"_run-0$run"/}
                    mv $ii $ii_new
                    mv ${ii/.json/.nii.gz} ${ii_new/.json/.nii.gz}
                    if [[ -f $ii_new ]];then
                    	echo '-----------Existing--------'
                    fi
                else
                	echo "DELETE"$ii
                	rm $ii
                	rm ${ii/.json/.nii.gz}
                fi
                #cat $ii | grep 'SeriesDescription'
            done
        done
    done
done

## rechecking fmaps:
datain='/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN'
for sub in $(ls $datain);do
    checkstatus=0
    for run in 7 6 5 4 3 2 1;do
	    for ii in $(find $datain'/'$sub -path '*dwi*' -iname '*.json*' -iname '*run-*' -iname "*run-0$run*");do
	    	echo $ii
	        if [[ $checkstatus == 0 ]];then
                checkstatus=1
          	    echo $sub, $run
                echo $ii
                ii_new=${ii/"_run-0$run"/}
                echo $ii_new
                if [[ -f $ii_new ]];then
                	echo '______________________'
                fi
                mv $ii $ii_new
                for type in .nii.gz .bval .bvec;do
                	echo $type
                	mv ${ii/.json/$type} ${ii_new/.json/$type} 
                done
            else
            	echo "-----DELETE-----"$ii
            	rm $ii
            	for type in .nii.gz .bval .bvec;do
                	rm ${ii/.json/$type}
                done
            fi
	    done
	done
done



### Final check the func intended for.
######### python scripts to put indented for into fmap json for dwi images. 
import json
import os
import numpy as np
dataout = '/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN'

for sub in os.listdir(dataout):
    if 'sub-' not in sub:
        continue
    #print(sub)
    indentedfor_list=[]
    for ses in os.listdir(dataout + '/' + sub ):
        
        ### dwi 
        if os.path.isdir(dataout + '/' + sub + '/' + ses + '/dwi'):
            for file in os.listdir(dataout + '/' + sub + '/' + ses + '/dwi'):
                if 'nii.gz' in file:
                    #print(file)
                    indentedfor  = ses + '/dwi/' + file
                    indentedfor_list.append(indentedfor)
        ### fmap
        if os.path.isdir(dataout + '/' + sub + '/' + ses + '/fmap'):
            for file in os.listdir(dataout + '/' + sub + '/' + ses + '/fmap'):
                if 'json' in file and 'acq-dwi' in file:
                    #print(file)
                    file_long=dataout + '/' + sub + '/' + ses + '/fmap/' + file
                    with open(file_long) as f:
                        data = json.load(f)
                    if 'IntendedFor' not in data.keys():
                        data['IntendedFor']=[]
                    if set(data['IntendedFor']) != set(indentedfor_list):
                        print(indentedfor_list)
                        print(data['IntendedFor'])

                        #data['IntendedFor']=indentedfor_list
                        #with open(file_long, 'w') as json_file:
                        #    json.dump(data, json_file,indent=4)

        ### fmri
        indentedfor_list=[]
        if os.path.isdir(dataout + '/' + sub + '/' + ses + '/func'):
            for file in os.listdir(dataout + '/' + sub + '/' + ses + '/func'):
                if 'nii.gz' in file:
                    #print(file)
                    indentedfor  = ses + '/func/' + file
                    indentedfor_list.append(indentedfor)
        ### fmap
        if os.path.isdir(dataout + '/' + sub + '/' + ses + '/fmap'):
            for file in os.listdir(dataout + '/' + sub + '/' + ses + '/fmap'):
                if 'json' in file and 'acq-fMRI' in file:
                    #print(file)
                    file_long=dataout + '/' + sub + '/' + ses + '/fmap/' + file
                    with open(file_long) as f:
                        data = json.load(f)
                    if 'IntendedFor' not in data.keys():
                        data['IntendedFor']=[]
                    if set(indentedfor_list) != set(data['IntendedFor']):
                        print('fMRI')
                        print(indentedfor_list)
                        print(data['IntendedFor'])

                        #data['IntendedFor']=indentedfor_list
                        #with open(file_long, 'w') as json_file:
                        #    json.dump(data, json_file,indent=4)




### check fmap names:
datain='/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN'

for i in $(ls /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/*/*/fmap/*.json);do

    if [[ $i == *"ses-HBNsiteSI"* ]];then continue;fi
    st=1
    xx=$(cat $i | grep SeriesDescription)

    if [[ $i == *"acq-fMRI"* ]] && [[ $xx == *"fMRI"* ]];then   
        st=0
    fi

    if [[ $i == *"acq-dwi"* ]] && [[ $xx == *"DKI"* ]];then   
        st=0

    fi    

    if [[ $i == *"acq-dwi"* ]] && [[ $xx == *"dMRI"* ]];then   
        st=0
    fi  

    if [[ $st == 1 ]];then
        i_new=${i/acq-dwi/acq-fMRI}
        if [[ ! -f $i_new ]];then
            mv $i $i_new
            mv ${i/.json/.nii.gz} ${i_new/.json/.nii.gz}
        fi
    fi
done

