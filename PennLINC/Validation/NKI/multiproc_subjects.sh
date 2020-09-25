#!/bin/bash

echo "subject,export_status,validator_status" > /storage/ttapera/RBC/PennLINC/Validation/NKI/output_status.csv

seq 1 1311 | xargs -P 15 -n 1 /storage/ttapera/RBC/PennLINC/Validation/NKI/export_status.sh
