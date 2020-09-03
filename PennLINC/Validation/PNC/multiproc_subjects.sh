#!/bin/bash

echo "subject,status" > /storage/ttapera/RBC/PennLINC/Validation/PNC/output_status.csv

seq 1 1601 | xargs -P 8 -n 1 /storage/ttapera/RBC/PennLINC/Validation/PNC/export_status.sh