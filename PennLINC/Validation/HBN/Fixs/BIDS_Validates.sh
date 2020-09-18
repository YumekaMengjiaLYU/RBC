# fw-heudiconv-validate --project RBC_HBN --subject sub-NDARKA331XEL --verbose


sublist='Wrong_file_name_sublist.txt'
sublist='Wrong_DWI_name_sublist.txt'
sublist='SliceTiming_sublist.txt'
sublist='Others_fmap_problems_sublist.txt'
sublist='Wrong_Missing_DWI_Data_sublist.txt'
sublist='ALL_SUBLIST.txt'
sublist='DWI_intendfor_no.txt'
sublist='NKI_Missing_Json.txt'

op='BIDS_Validate_output'
mkdir -p $op
for sub in $(cat $sublist);do
    echo $sub
    #fw-heudiconv-validate --project RBC_HBN --subject $sub --verbose  >>$op'/'$sub'.txt' 2>&1
    fw-heudiconv-validate --project RBC_NKI --subject $sub --verbose  >>$op'/'$sub'.txt' 2>&1

done



# scp /Users/lei.ai/Dropbox/Work\&Study/projects/HBN_data/Flywheel/RBC/PennLINC/Validation/HBN/Fixs2/*.csv  lai@ned.childmind.org:/data2/HBNcore/CMI_HBN_Data/Scripts/Send_2_collab/Flywheel_project/RBC_Fix_09152020/.



# check resutls

d=/Users/lei.ai/Dropbox/Work\&Study/projects/HBN_data/Flywheel/RBC/PennLINC/Validation/HBN/Fixs2/BIDS_Validate_output
for i in $(ls $d);do 
	#echo $i; 
	errinfo=$(cat $d'/'$i | grep ERR); 
	warninfo=$(cat $d'/'$i | grep WARN);
    if [[ ! -z $errinfo ]];then
    	echo $i
    fi

done