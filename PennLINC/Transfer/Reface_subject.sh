#! /bin/bash

# input: row of a csv with BBLID, HASH, FULL-ID
line=$1

# parse this input row
info=$(cat /storage/ttapera/RBC/data/bblids_3.csv | head -n $line | tail -n 1 | sed 's/,/ /g')

echo $info

bblid=$(echo $info | cut -d ' ' -f 1)
hash=$(echo $info | cut -d ' ' -f 2)
subject=$(echo $info | cut -d ' ' -f 3)

echo $bblid
echo $hash
echo $subject
echo
echo downloading from RBC
echo fw-heudiconv-export --project PNC_CS_810336 --subject $bblid --destination /storage/ttapera/RBC/data/$subject
echo
#for filename in $(ls /storage/ttapera/RBC/data/$subject/bids_dataset/sub-*/ses-*/*/*T1w.nii.gz); do

for i in $(ls /storage/ttapera/RBC/data/$subject/bids_directory/sub-*/ses-*/*/*.nii.gz)
do
    echo mv "$i" "${i//$bblid/$hash}"
done