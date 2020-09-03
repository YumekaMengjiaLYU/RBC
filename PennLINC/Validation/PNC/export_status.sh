#!/bin/bash

# input: row of file
line=$1

# parse this input row
info=$(cat /storage/ttapera/RBC/PennLINC/Validation/PNC/pnc_subjects.txt | head -n $line | tail -n 1)

fw export bids --project RBC_PNC --subject $info /storage/ttapera/RBC/data/validation/PNC/bids_dataset/
status=$?
echo "$info,$status" >> output_status.csv