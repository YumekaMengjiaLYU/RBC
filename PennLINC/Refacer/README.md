# PennLINC Refacer Documentation & Usage

**Goal**: Upload BIDS valid datasets to the RBC project on Flywheel

**Challenge**: Defacing

We have attempted a few different ways of de-identifying our data via defacing;
some confusion has forced us to unify our efforts and only stick to one model.
We have decided to use the `afni_refacer` approach which showed significant
stability and success over other options.

Unfortunately, many sites have already uploaded data to Flywheel, and the task
of deleting and re-uploading this data is cumbersome for many. A better approach
is to just deface the T1w locally and replace the file that is on Flywheel. The
Python script in this repo helps to accomplish that.

**Solution**: A python script that scans an existing BIDS dataset on disk,
checks to see if this data exists in the RBC project, and then, on disk, preps
and refaces a T1w image and uploads it to the target acquisition on Flywheel.

**Methods**: This script introduces FlyBIDS, a lightweight and easy-to-use BIDS
tool for quickly building and inspecting Flywheel BIDS data. The functionality
introduced by FlyBIDS is intended to be identical to that of PyBIDS. By comparing
the output of a FlyBIDS dataset on Flywheel to a PyBIDS dataset on disk, we're
able to quickly navigate and operate on two disparete datasets with ease.
Additionally, we use Docker to wrap `afni_refacer` for version stability across
sites.

---

# Installation

This script requires that you have [Docker](https://www.docker.com/get-started) installed on your machine.

Once you have Docker running, pull the PennLINC image for `afni_refacer` by doing:

```
docker pull pennlinc/afni_refacer
```

Next, you need the Python packages. We recommend just starting a new virtual
environment for this, e.g. with `conda`:

```
conda create -n rbc python=3.7
conda activate rbc
```

Then we install the packages necessary with `pip`:

```
# cd to this directory first if necessary
pip install -r requirements.txt
```

# Usage
```
usage: PennLINC_Refacer.py [-h] [--project PROJECT] --directory DIRECTORY
                           [--rec REC] [--verbose] [--dry-run] [--delete]
                           [--api-key API_KEY]

Reface T1w scan and upload it to Flywheel

optional arguments:
  -h, --help            show this help message and exit
  --project PROJECT     The project on Flywheel
  --directory DIRECTORY
                        Path to existing BIDS directory on disk with a T1w to
                        be refaced
  --rec REC             The value to put in the new filename for the BIDS
                        field rec-<value>
  --verbose             Print ongoing messages of progress
  --dry-run             Don't apply changes
  --delete              Delete original file on Flywheel.
  --api-key API_KEY     API Key
```

In this example I'll reface one of the files in our `gear_testing` project.
I already have the original BIDS NIfTI data on my disk, so that's what goes in the
`--directory` flag. The `--rec` flag refers to a BIDS valid value to insert into
the new BIDS name (defaults to `refaced`). The `--delete` flag is an optional one that *will delete the
original T1w file from Flywheel; use with caution* (test without first).

```
python PennLINC_Refacer.py --project gear_testing --directory ../../data/bids_directory/ --verbose --dry-run
```

When used in `--dry-run` the script simply creates a copy of the T1. You can now
inspect your BIDS directory to ensure it found all of the correct files and meant
to reface the correct ones.

```
(rbc) tinashetapera2:Refacer ttapera$ tree ../../data/bids_directory/
../../data/bids_directory/
├── dataset_description.json
├── sub-1832999514
│   ├── ses-PNC1
│   │   ├── anat
│   │   │   ├── sub-1832999514_ses-PNC1_T1w.json
│   │   │   ├── sub-1832999514_ses-PNC1_T1w.nii.gz
│   │   │   └── sub-1832999514_ses-PNC1_rec-refaced_T1w.nii.gz # GOOD !
│   │   └── func
│   │       ├── sub-1832999514_ses-PNC1_task-rest_acq-singleband_bold.json
│   │       └── sub-1832999514_ses-PNC1_task-rest_acq-singleband_bold.nii.gz
│   └── ses-PNC2
│       ├── anat
│       │   ├── sub-1832999514_ses-PNC2_T1w.json
│       │   ├── sub-1832999514_ses-PNC2_T1w.nii.gz
│       │   └── sub-1832999514_ses-PNC2_rec-refaced_T1w.nii.gz # GOOD!
│       ├── fmap
│       │   ├── sub-1832999514_ses-PNC2_magnitude1.json
│       │   ├── sub-1832999514_ses-PNC2_magnitude1.nii.gz
│       │   ├── sub-1832999514_ses-PNC2_magnitude2.json
│       │   ├── sub-1832999514_ses-PNC2_magnitude2.nii.gz
│       │   ├── sub-1832999514_ses-PNC2_phase1.json
│       │   ├── sub-1832999514_ses-PNC2_phase1.nii.gz
│       │   ├── sub-1832999514_ses-PNC2_phase2.json
│       │   └── sub-1832999514_ses-PNC2_phase2.nii.gz
│       └── func
│           ├── sub-1832999514_ses-PNC2_task-frac2back.json
│           ├── sub-1832999514_ses-PNC2_task-frac2back.nii.gz
│           ├── sub-1832999514_ses-PNC2_task-idemo.json
│           ├── sub-1832999514_ses-PNC2_task-idemo.nii.gz
│           ├── sub-1832999514_ses-PNC2_task-rest_acq-singleband_bold.json
│           └── sub-1832999514_ses-PNC2_task-rest_acq-singleband_bold.nii.gz
└── sub-2216595430
    └── ses-PNC1
        ├── anat
        │   ├── sub-2216595430_ses-PNC1_T1w.json
        │   ├── sub-2216595430_ses-PNC1_T1w.nii.gz
        │   └── sub-2216595430_ses-PNC1_rec-refaced_T1w.nii.gz # GOOD!
        ├── fmap
        │   ├── sub-2216595430_ses-PNC1_phasediff.json
        │   └── sub-2216595430_ses-PNC1_phasediff.nii.gz
        └── func
            ├── sub-2216595430_ses-PNC1_task-frac2back_run-01.json
            ├── sub-2216595430_ses-PNC1_task-frac2back_run-01.nii.gz
            ├── sub-2216595430_ses-PNC1_task-frac2back_run-02.json
            ├── sub-2216595430_ses-PNC1_task-frac2back_run-02.nii.gz
            ├── sub-2216595430_ses-PNC1_task-idemo.json
            ├── sub-2216595430_ses-PNC1_task-idemo.nii.gz
            ├── sub-2216595430_ses-PNC1_task-rest_acq-singleband_bold.json
            └── sub-2216595430_ses-PNC1_task-rest_acq-singleband_bold.nii.gz
```

After running without the `--dry-run` flag, you should also see data leftover in
your BIDS directory from the refacing:
```
└── sub-2216595430
    └── ses-PNC1
        ├── anat
        │   ├── sub-2216595430_ses-PNC1_T1w.json
        │   ├── sub-2216595430_ses-PNC1_T1w.nii.gz
        │   ├── sub-2216595430_ses-PNC1_rec-refaced_T1w.face.nii.gz
        │   ├── sub-2216595430_ses-PNC1_rec-refaced_T1w.nii.gz
        │   └── sub-2216595430_ses-PNC1_rec-refaced_T1w_QC
        │       ├── sub-2216595430_ses-PNC1_rec-refaced_T1w.axi.png
        │       ├── sub-2216595430_ses-PNC1_rec-refaced_T1w.cor.png
        │       ├── sub-2216595430_ses-PNC1_rec-refaced_T1w.face.axi.png
        │       ├── sub-2216595430_ses-PNC1_rec-refaced_T1w.face.cor.png
        │       ├── sub-2216595430_ses-PNC1_rec-refaced_T1w.face.sag.png
        │       └── sub-2216595430_ses-PNC1_rec-refaced_T1w.sag.png
```

---

# Alternative: Replacing BIDS Data

If you prefer to use the `afni_refacer` tool in isolation and just re-upload all of your data, you can also do that with the docker image:

```
docker run -t --rm --user $(id -u):$(id -g) \
    -v /FULL/PATH/TO/BIDS/ANAT/FOLDER/:/home/ \
    pennlinc/afni_refacer \
    -input /home/sub-<SUBJECT>_ses-<SESSION>_T1w.nii.gz \
    -mode_reface \
    -prefix /home/sub-<SUBJECT>_ses-<SESSION>_rec-refaced_T1w.nii.gz
```
You can use the SDK to then remove the existing subject on Flywheel and re-upload them.
