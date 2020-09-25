#!/bin/bash

echo "subject,export_status,validator_status" > /storage/ttapera/RBC/PennLINC/Validation/HBN/output_status.csv

seq 1 2618 | xargs -P 15 -n 1 /storage/ttapera/RBC/PennLINC/Validation/HBN/export_status.sh
