#! /bin/bash

# input: row of a csv with BBLID, HASH, FULL-ID
line=$1

# parse this input row
info=$(cat /storage/ttapera/RBC/data/bblids_3.csv | head -n $line | tail -n 1 | sed 's/,/ /g')

echo $info

# get a subject variable (for later use)
SourceSubject=$(echo $info | cut -d ' ' -f 1)
TargetSubject=$(echo $info | cut -d ' ' -f 2)

mkdir /storage/ttapera/RBC/data/$SourceSubject

# download the bids for this subject
fw export bids /storage/ttapera/RBC/data/$SourceSubject --project PNC_CS_810336 --subject $SourceSubject --data-type dwi

download_status=$?

# rename
python /storage/ttapera/RBC/PennLINC/Transfer/renameDWI.py $info
rename_status=$?

# upload data
echo uploading...
yes | fw import bids --quiet --project RBC_PNC --subject sub-$TargetSubject /storage/ttapera/RBC/data/$SourceSubject/ bbl

upload_status=$?

# remove dir
echo removing...
rm -rf /storage/ttapera/RBC/data/$SourceSubject
    
# save progress
echo "$TargetSubject,$download_status,$rename_status,$upload_status,$(date)" >> /storage/ttapera/RBC/data/dwi_uploaded_09092020.txt
