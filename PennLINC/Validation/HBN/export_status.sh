#!/bin/bash

# input: row of file
line=$1

# parse this input row
info=$(cat /storage/ttapera/RBC/PennLINC/Validation/HBN/hbn_subjects2.txt | head -n $line | tail -n 1)

mkdir -p /storage/ttapera/RBC/data/validation/HBN/$info/bids_directory

#fw-heudiconv-validate --project RBC_HBN --subject $info --directory /storage/ttapera/RBC/data/validation/HBN/$info --tabulate /storage/ttapera/RBC/data/validation/HBN/$info

fw export bids -y --project RBC_HBN --subject $info /storage/ttapera/RBC/data/validation/HBN/$info/bids_directory
export_status=$?

bids-validator --json --verbose /storage/ttapera/RBC/data/validation/HBN/$info/bids_directory > /storage/ttapera/RBC/data/validation/HBN/$info/issues.json
#python validate_parse.py /storage/ttapera/RBC/data/validation/HBN/$info/
validator_status=$?

echo "$info,$export_status,$validator_status" >> output_status.csv

rm -rf /storage/ttapera/RBC/data/validation/HBN/$info/bids_directory