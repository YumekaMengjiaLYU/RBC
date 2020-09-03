#!/bin/bash

echo "subject,status" > /storage/ttapera/RBC/PennLINC/Validation/NKI/output_status.csv

seq 1 1312 | xargs -P 10 -n 1 /storage/ttapera/RBC/PennLINC/Validation/NKI/export_status.sh