echo "subject,download_ok,rename_ok,upload_ok,date" > /storage/ttapera/RBC/data/dwi_uploaded_09092020.txt
seq 1 1601 | xargs -P 15 -n 1 /storage/ttapera/RBC/PennLINC/Transfer/transfer_dwi_subject.sh