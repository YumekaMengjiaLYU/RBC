#!/bin/bash

# input: row of file
line=$1

# parse this input row
info=$(cat /storage/ttapera/RBC/PennLINC/Validation/NKI/nki_subjects.txt | head -n $line | tail -n 1)

fw export bids --project RBC_NKI --subject $info /storage/ttapera/RBC/data/validation/NKI/bids_dataset/
status=$?
echo "$info,$status" >> output_status.csv