#!/bin/bash

line=$1

fw import bids --debug --project RBC_HBN_cubic --subject $line /cbica/projects/RBC/flywheel_curation/RBC/data/bids_datasets/RBC_HBN/ bbl

#while read line; do
#  qsub-run 
  
#done < /cbica/projects/RBC/flywheel_curation/RBC/PennLINC/Validation/CUBIC_Curation/upload_ready_subject_lists/hbn_upload.txt

