#!/bin/bash

# input: row of file
line=$1

# parse this input row
info=$(cat /storage/ttapera/RBC/PennLINC/Validation/HBN/hbn_subjects.txt | head -n $line | tail -n 1)

mkdir /storage/ttapera/RBC/data/validation/HBN/$info

fw-heudiconv-validate --project RBC_HBN --subject $info --directory /storage/ttapera/RBC/data/validation/HBN/$info --tabulate /storage/ttapera/RBC/data/validation/HBN/$info

status=$?
echo "$info,$status" >> output_status.csv