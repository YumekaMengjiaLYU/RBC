### download to cubic.sh ###

project=$1
subject=$2

fw export bids --project $project --subject $subject $HOME/RBC_RAWDATA/bidsdatasets/$project
