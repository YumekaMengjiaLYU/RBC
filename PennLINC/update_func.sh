#! /bin/bash

while IFS=, read -r bblid hash fullid process
do
    if [ $process == 'True' ]
    then
        echo "$bblid | $hash"
        
        echo Downloading...
        
        python /storage/ttapera/RBC/PennLINC/download_bids.py $bblid $hash $fullid
        
        for filename in /storage/ttapera/RBC/data/upload/sub-*/*/*/*T1w.nii.gz; do
            
            base=$(basename "$filename")
            echo Defacing $basename ...
            docker run --rm --user "$(id -u):$(id -g)" -v $filename:/data/$base pennbbl/mrideface /data/$base /opt/mrideface/talairach_mixed_with_skull.gca /opt/mrideface/face.gca /data/$base
        done
        
        echo uploading...
        yes | fw import bids --project ReproBrainChart /storage/ttapera/RBC/data/upload/ bbl
        
        echo removing...
        rm -rf /storage/ttapera/RBC/data/upload/*
        rm -rf /storage/ttapera/RBC/data/PNC*
        
        echo "$bblid, $hash" >> /storage/ttapera/RBC/data/completed.txt
        
    fi
done < /storage/ttapera/RBC/data/bblids_2.csv
