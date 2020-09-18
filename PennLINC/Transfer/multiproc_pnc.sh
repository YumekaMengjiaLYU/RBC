echo "subject,download_ok,rename_ok,upload_ok,date" > /storage/ttapera/RBC/data/asl_uploaded2_17092020.txt
seq 1 419 | xargs -P 15 -n 1 /storage/ttapera/RBC/PennLINC/Transfer/transfer_asl_subject.sh