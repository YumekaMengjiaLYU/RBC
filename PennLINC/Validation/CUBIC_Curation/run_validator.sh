#!/bin/bash

time bids-validator --json --verbose /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/PNC > pnc_issues.json &

time bids-validator --json --verbose /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/NKI > nki_issues.json &

time bids-validator --json --verbose /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN > hbn_issues.json &