#!/bin/bash

# input: row of file
line=$1

# parse this input row
info=$(cat /storage/ttapera/RBC/PennLINC/Validation/PNC/pnc_subjects.txt | head -n $line | tail -n 1)

mkdir /storage/ttapera/RBC/data/validation/PNC/$info

fw-heudiconv-validate --project RBC_PNC --subject $info --directory /storage/ttapera/RBC/data/validation/PNC/$info --tabulate /storage/ttapera/RBC/data/validation/PNC/$info

status=$?
echo "$info,$status" >> output_status.csv