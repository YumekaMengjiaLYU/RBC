#echo "subject,download_ok,check_ok,date" > /storage/ttapera/RBC/data/completed.txt
seq 2 885 | xargs -P 10 -n 1 /storage/ttapera/RBC/PennLINC/process_subject.sh