#!/bin/bash

# run validator
time bids-validator --json --verbose --ignoreSessionConsistency /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/PNC > pnc_issues.json

time bids-validator --json --verbose --ignoreSessionConsistency /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/NKI > nki_issues.json

time bids-validator --json --verbose --ignoreSessionConsistency /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN > hbn_issues.json