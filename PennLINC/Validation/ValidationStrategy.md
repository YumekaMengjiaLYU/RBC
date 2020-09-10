# Validating RBC

There are two steps to validation of the RBC project. The first is ensuring the data can be exported correctly (i.e. all BIDS files are present and not duplicates). This is completed in each project by calling the script `multiproc_subject.sh`, which calls the `fw export bids` CLI on the list of subjects. It tracks exit status to ensure each subject is good to go. The data in this case is being exported to the following directory structure:

```
.
├── data                  # NOT VERSION CONTROLLED
│   └── validation        # ALL RAW DATA EXPORTED HERE
│       ├── PNC
│       │   └── bids_dataset
│       ├── RBC
│       │   └── bids_dataset
│       └── NKI
│           └── bids_dataset
│
├── Deface_and_refine
│   └── mri_deface
└── PennLINC
    ├── Refacer
    └── Validation
        ├── PNC
        ├── RBC
        └── NKI
```

The next step is running the validator and exporting the validation results. With the BIDS-validator CLI, run the validator in `--json` and `--verbose` modes, and pipe that result to a file:

```
bids-validator ./data/validation/PNC/bids_dataset/ --json --verbose > ./PennLINC/Validation/PNC/validation.json
```

The final stage is parsing this output into useful warnings and errors. You can use Python to do this:

```
import json
import pandas as pd

def parse_validator(path):

    with open(path, 'r') as read_file:
        data = json.load(read_file)

    issues = data['issues']

    def parse_issue(issue_dict):

        return_dict = {}
        return_dict['files'] = [get_nested(x, 'file', 'relativePath') for x in issue_dict.get('files', '')]
        return_dict['type'] = issue_dict.get('key' '')
        return_dict['severity'] = issue_dict.get('severity', '')
        return_dict['description'] = issue_dict.get('reason', '')
        return_dict['code'] = issue_dict.get('code', '')
        return_dict['url'] = issue_dict.get('helpUrl', '')

        return(return_dict)

    df = pd.DataFrame()

    for warn in issues['warnings']:

        parsed = parse_issue(warn)
        parsed = pd.DataFrame(parsed)
        df = df.append(parsed, ignore_index=True)

    for err in issues['errors']:

        parsed = parse_issue(err)
        parsed = pd.DataFrame(parsed)
        df = df.append(parsed, ignore_index=True)

    return df
    
path = './PennLINC/Validation/PNC/validation.json'

validation_df = parse_validator(path)

validation_df.shape

validation_df.to_csv('./PennLINC/Validation/PNC/validation.csv')
```

The data can be viewed in any CSV viewer; the end goal is to keep working until all issues are attended to. Each dataset's adjustment scripts are kept in their respective directories.

---

To run the BIDS validator in parallel on Flywheel, you can use something like the following script:

```
import flywheel
import datetime


```