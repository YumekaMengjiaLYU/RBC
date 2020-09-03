#!/bin/bash

# input: row of file
line=$1

# parse this input row
info=$(cat /storage/ttapera/RBC/data/validation/HBN/hbn_subjects.txt | head -n $line | tail -n 1)

fw export bids --project RBC_HBN --subject $info bids_dataset/
status=$?
echo "$info,$status" >> output_status.csv
