#! /bin/bash

### use the SGE to download data in parallel

project=$1
subject_list=$2

while read p; do
  qsub $HOME/flywheel_curation/RBC/PennLINC/Validation/export_subject.sh $project "$p"
done < $subject_list
