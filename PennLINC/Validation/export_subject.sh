### download to cubic.sh ###

project=$1
subject=$2

fw export bids --project $project --subject $subject $HOME/flywheel_curation/RBC/data/bids_datasets/$project
