#! /bin/bash

# input: row of a csv with BBLID, HASH, FULL-ID
line=$1

# parse this input row
info=$(cat /storage/ttapera/RBC/data/bblids_3.csv | head -n $line | tail -n 1 | sed 's/,/ /g')

echo $info

# download the bids for this subject
python /storage/ttapera/RBC/PennLINC/download_bids.py $info
download_status=$?
python /storage/ttapera/RBC/PennLINC/clean_and_check.py $info
check_status=$?

# get a subject variable (for later use)
subject=$(echo $info | cut -d ' ' -f 2)

# deface each T1w image
for filename in $(ls /storage/ttapera/RBC/data/$subject/bids_dataset/sub-*/*/*/*T1w.nii.gz); do
    
    # Do some gymnastics to save the output file as acq-defaced
    base=$(basename "$filename")
    dir=$(dirname "$filename")
    matchPNC="PNC1_"
    acq="acq-refaced_"
    
    output=$(echo "$base" | sed "s/$matchPNC/&$acq/g")
    
    # Do some gymnastics to also create a sidecar for this new file
    file=$(basename "$filename" .nii.gz)
    sidecarExt=".json"
    sidecarOriginal=$dir/$file$sidecarExt
    sidecarDefaced=$(echo "$sidecarOriginal" | sed "s/$matchPNC/&$acq/g")
    
    echo Defacing $filename ... as $output with sidecar $sidecarDefaced
    #echo time @afni_refacer_run -input $filename -mode_deface -prefix $dir/$output
    time docker run -t --rm --user $(id -u):$(id -g) \
        -v $dir/:/home/ \
        pennlinc/afni_refacer \
        -input /home/$base \
        -mode_reface \
        -prefix /home/$output
    # copy sidecar
    cp $sidecarOriginal $sidecarDefaced
    
    # clean deface data
    rm -rf $dir/*_QC
    rm $dir/*.face.nii.gz
    rm $dir/$base
    rm $sidecarOriginal

done

# upload data
echo uploading...
yes | fw import bids --quiet --project ReproBrainChart /storage/ttapera/RBC/data/$subject/bids_dataset/ bbl

# remove dir
echo removing...
rm -rf /storage/ttapera/RBC/data/$subject
    
# save progress
echo "$subject,$download_status,$check_status,$(date)" >> /storage/ttapera/RBC/data/completed_2020-07-14.txt
