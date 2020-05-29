#! /bin/bash


line=$1
info=$(cat /storage/ttapera/RBC/data/bblids_3.csv | head -n $line | tail -n 1 | sed 's/,/ /g')

echo $info

python /storage/ttapera/RBC/PennLINC/download_and_clean_bids.py $info

subject=$(echo $info | cut -d ' ' -f 2)

for filename in $(ls /storage/ttapera/RBC/data/$subject/bids_dataset/sub-*/*/*/*T1w.nii.gz); do
            
    base=$(basename "$filename")
    
    echo Defacing $filename ...
    docker run --rm --user "$(id -u):$(id -g)" -v $filename:/data/$base pennbbl/mrideface /data/$base /opt/mrideface/talairach_mixed_with_skull.gca /opt/mrideface/face.gca /data/$base
done
    
echo uploading...
yes | fw import bids --quiet --project ReproBrainChart /storage/ttapera/RBC/data/$subject/bids_dataset/ bbl
    
echo removing...
rm -rf /storage/ttapera/RBC/data/$subject
    
echo "$bblid, $hash, $(date)" >> /storage/ttapera/RBC/data/completed.txt
