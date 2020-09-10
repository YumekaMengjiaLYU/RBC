#!/bin/bash

# input: row of file
line=$1

# parse this input row
info=$(cat /storage/ttapera/RBC/PennLINC/Validation/NKI/nki_subjects.txt | head -n $line | tail -n 1)

mkdir /storage/ttapera/RBC/data/validation/NKI/$info

fw-heudiconv-validate --project RBC_NKI --subject $info --directory /storage/ttapera/RBC/data/validation/NKI/$info --tabulate /storage/ttapera/RBC/data/validation/NKI/$info

status=$?
echo "$info,$status" >> output_status.csv