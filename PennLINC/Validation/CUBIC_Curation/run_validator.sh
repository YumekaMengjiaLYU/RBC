#!/bin/bash

# change permissions to write only
find /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/PNC -type f -iname "*" -print0 | xargs -I {} -0 chmod 444 {}

find /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/NKI -type f -iname "*" -print0 | xargs -I {} -0 chmod 444 {}

find /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN -type f -iname "*" -print0 | xargs -I {} -0 chmod 444 {}

# run validator
time bids-validator --json --verbose --ignoreSessionConsistency /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/PNC > pnc_issues.json

time bids-validator --json --verbose --ignoreSessionConsistency /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/NKI > nki_issues.json

time bids-validator --json --verbose --ignoreSessionConsistency /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN > hbn_issues.json

# revert permissions
find /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/NKI -type f -iname "*" -print0 | xargs -I {} -0 chmod 644 {}

find /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/PNC -type f -iname "*" -print0 | xargs -I {} -0 chmod 644 {}

find /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN -type f -iname "*" -print0 | xargs -I {} -0 chmod 644 {}