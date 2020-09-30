#!/bin/bash

line=$1

echo fw import bids --debug --project RBC_NKI_cubic --subject $line /cbica/projects/RBC/flywheel_curation/RBC/data/bids_datasets/RBC_NKI/ bbl

#while read line; do
#  qsub-run 
  
#done < /cbica/projects/RBC/flywheel_curation/RBC/PennLINC/Validation/NKI/nki_subjects2.txt