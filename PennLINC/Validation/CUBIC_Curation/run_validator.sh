#!/bin/bash

bids-validator --json --verbose /cbica/projects/RBC/flywheel_curation/RBC/data/bids_datasets/RBC_PNC > pnc_issues.json &

bids-validator --json --verbose /cbica/projects/RBC/flywheel_curation/RBC/data/bids_datasets/RBC_NKI > nki_issues.json &

bids-validator --json --verbose /cbica/projects/RBC/flywheel_curation/RBC/data/bids_datasets/RBC_HBN > hbn_issues.json &