#!/bin/bash

echo "subject,status" > /storage/ttapera/RBC/PennLINC/Validation/HBN/output_status.csv

seq 1 2680 | xargs -P 15 -n 1 /storage/ttapera/RBC/PennLINC/Validation/HBN/export_status.sh