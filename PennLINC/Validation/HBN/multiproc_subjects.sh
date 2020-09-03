#!/bin/bash

echo "subject,status" > /storage/ttapera/RBC/data/validation/HBN/output_status.csv

seq 1 2680 | xargs -P 15 -n 1 /storage/ttapera/RBC/data/validation/HBN/export_status.sh