#!/usr/bin/env python

from tqdm import tqdm
import bids.layout
import bids
from collections import defaultdict
from bids.utils import listify
from pathlib import Path
import json
bids.config.set_option('extension_initial_dot', True)

suffix = '(phase2|magnitude1|magnitude2|phase1|phasediff|epi|fieldmap)'
bids_path = '/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/PNC'
layout = bids.BIDSLayout(bids_path)

fmap_jsons = layout.get(suffix=suffix, regex_search=True, extension='.json')


files_to_fmaps = defaultdict(list)

for fmap_json in tqdm(fmap_jsons):

    sub = "sub-%s" % fmap_json.entities['subject']
    ses = "ses-%s" % fmap_json.entities['session']

    full_path = bids_path + '/' + sub + '/' + ses + '/' + 'fmap/' + fmap_json.filename
    print(full_path)

    with open(full_path) as f:
        data = json.load(f)

    # remove asl references in the IntendedFor
    for item in data['IntendedFor']:
        if 'perf' in item:
            data['IntendedFor'].remove(item)
            print(data['IntendedFor'])

    # replace the IntendedFor list of files with the new list
    with open(full_path, 'w') as file:
        json.dump(data, file, indent=4)
