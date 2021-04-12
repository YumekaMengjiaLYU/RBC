# Data Narrative

This file describes how the data was curated into BIDS after it was de-identified.
For more details, see the commit history of this repository.

Note: In this special case, original data is stored in
`/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN`

# Transfer Process

The data were acquired at [SITE] as part of the Healthy Brain Network study
[CITATION]. Access was given to PennLINC as part of the Reproducible Brain
Chart project [CITATION]. The data was first refaced at all local sites using
[`afni_refacer`](https://github.com/PennLINC/RBC/blob/master/PennLINC/Validation/CUBIC_Curation/Notebooks/FixingHBN.ipynb). The software is containerized in [Docker](https://hub.docker.com/repository/docker/pennlinc/afni_refacer).
Data was then imported from [SITE] to Flywheel. The approximate date of
transfer was July 2020. In sum, PennLINC received approximately [VOLUME]
comprising of [N] subjects and [N] individual sessions (with session labels
ranging from [SESLABEL] to [SESLABEL]). The imaging data consisted of [MODALITIES].
Task data consisted of [TASKS].

\#TODO LA could you fill in the [SITE] and [CITATION] for HBN acquisition?

No additional cohort data was provided at this time of transfer. The imaging data was
organized in BIDS and anonymized at the time of transfer.

<div style="text-align: right"> — TT </div>

# BIDS Curation

BIDS curation was initially accomplished with BIDS validator version `< 1.5`.
Generally, we found that this version could open data and corrupt files, or
misread files due to Java memory buffer limits, and not report this problem.
Hence, occasionally errors were introduced to the dataset after not being
previously present.

<div style="text-align: right"> — TT </div>

On [2020-09-10](https://github.com/PennLINC/RBC/blob/e2eea9f2680cbcf1f40261c4f1cc6622c1d1b491/PennLINC/Validation/Merging.ipynb), the following errors were found:

DWI_MISSING_BVAL: 7 subjects

NOT_INCLUDED: 122 files

PHASE_ENCODING_DIRECTION_MUST_DEFINE: 107 files

QUICK_VALIDATION_FAILED: 56 subjects

SLICETIMING_VALUES_GREATOR_THAN_REPETITION_TIME: 18 files

TOTAL_READOUT_TIME_MUST_DEFINE: 107 files

VOLUME_COUNT_MISMATCH: 1 subject

EVENTS_TSV_MISSING: 8563 files

INCONSISTENT_PARAMETERS: 38 subjects

NO_AUTHORS

README_FILE_MISSING

SLICETIMING_ELEMENTS: 147 files

\#TODO Were there any scripts used to remedy these?


---

On [2020-09-17](https://github.com/PennLINC/RBC/blob/a343683fc023e9fc426264c95671c9f95ef0e51a/PennLINC/Validation/Merging.ipynb), the BIDS validation result was:

INTENDED_FOR: 2 subjects

QUICK_VALIDATION_FAILED: 56 subjects

EVENTS_TSV_MISSING: 8583 files

INCONSISTENT_PARAMETERS: 38 files

NO_AUTHORS

README_FILE_MISSING

SLICETIMING_ELEMENTS: 1 file

\#TODO LA: Were there any scripts used to remedy these?

---

On 2020-09-24, the BIDS validation result was:

NOT_INCLUDED: 98 files

EVENTS_TSV_MISSING: 8622 files

INCONSISTENT_PARAMETERS: 38 files

NO_AUTHORS

README_FILE_MISSING

\#TODO Were there any scripts used to remedy these?

---

At this point, we changed to validator version `1.5.7-dev.0`, as it allowed us
to include NIfTI header information accurately and was less likely to corrupt or
misread data. This version revealed more errors but remains stable.

On [2020-09-25](https://nbviewer.jupyter.org/github/PennLINC/RBC/blob/11f7d67d673cdf99c826313dd5986c714c57504d/PennLINC/Validation/Merging.ipynb) the BIDS validation result was:

DATASET_DESCRIPTION_JSON_MISSING

DWI_MISSING_BVEC: 1 subject

EMPTY_FILE: 1 file

NOT_INCLUDED:	4 files

PHASE_ENCODING_DIRECTION_MUST_DEFINE:	4 files

REPETITION_TIME_MUST_DEFINE:	7 files

TASK_NAME_MUST_DEFINE:	7 files

TOTAL_READOUT_TIME_MUST_DEFINE:	4 files

ECHO_TIME_NOT_DEFINED:	8 files

EFFECTIVE_ECHO_SPACING_NOT_DEFINED:	8 files

EVENTS_TSV_MISSING:	8622 files

INCONSISTENT_PARAMETERS:	38 files

NO_AUTHORS

PHASE_ENCODING_DIRECTION_NOT_DEFINED:	8 files

README_FILE_MISSING

SLICE_TIMING_NOT_DEFINED:	7 files

TOTAL_READOUT_TIME_NOT_DEFINED:	1 files

Many of these were solved by re-running the downloads from Flywheel in [this notebook](https://nbviewer.jupyter.org/github/PennLINC/RBC/blob/master/PennLINC/Validation/CUBIC_Curation/Notebooks/FixingHBN.ipynb) from 2020-09-30 and fixing naming structures in [this notebook](https://github.com/PennLINC/RBC/blob/master/PennLINC/Validation/HBN/FIxesNotebooks/Renaming_EPI_Files_24092020.ipynb) from 2020-09-24.

---

After the above notebooks, the validator errors were as follows on [2020-10-02](https://github.com/PennLINC/RBC/blob/bd0f09eaed669a5ca5e26a95c9deb099d19615ec/PennLINC/Validation/Merging.ipynb):

57 -- DATASET_DESCRIPTION_JSON_MISSING

18 -- PHASE_ENCODING_DIRECTION_MUST_DEFINE: 3401 files

10 -- REPETITION_TIME_MUST_DEFINE: 5541 files

50 -- TASK_NAME_MUST_DEFINE: 5541 files

19 -- TOTAL_READOUT_TIME_MUST_DEFINE: 3401 files

6 -- ECHO_TIME_NOT_DEFINED: 6196 files

8 -- EFFECTIVE_ECHO_SPACING_NOT_DEFINED: 6196 files

25 -- EVENTS_TSV_MISSING: 3858 files

39 -- INCONSISTENT_PARAMETERS: 231 files

38 -- INCONSISTENT_SUBJECTS: 22842 files

97 -- MISSING_SESSION: 1035 files

7 -- PHASE_ENCODING_DIRECTION_NOT_DEFINED: 6196 files

101 -- README_FILE_MISSING

13 -- SLICE_TIMING_NOT_DEFINED: 5541 files

9 -- TOTAL_READOUT_TIME_NOT_DEFINED: 655 files

\#TODO LA: Were there any scripts used to remedy these?

---

The validator was run again on [2020-10-13](https://github.com/PennLINC/RBC/blob/ddeed5494eaadf136e89b7da060378946789d8cc/PennLINC/Validation/Merging.ipynb):

25 -- EVENTS_TSV_MISSING:	8627 files

39 -- INCONSISTENT_PARAMETERS:	621 files

113 -- NO_AUTHORS

101 -- README_FILE_MISSING

This same result was obtained when run on [2020-10-14](https://github.com/PennLINC/RBC/blob/afcd0e93de6c20c244761e7676735444e671b98a/PennLINC/Validation/Merging.ipynb) and [2020-10-16](https://github.com/PennLINC/RBC/blob/fee24be51182cfa6b5655c7042933a0882a3b8b8/PennLINC/Validation/Merging.ipynb).

<div style="text-align: right"> — TT </div>

---

\#TODO LA can you confirm these details or elabourate where useful? Any scripts available in Github?

On December, 2020, we identified missing and empty nifti files, and asked LA to upload/replace. On January, 2021, Lei changed names of fieldmap files. We then ran `add_nifti_info.py` on the dataset (now a `cubids` tool) to ensure all the
data was complete. On Jan 28, 2021 we identified dwi and bold scans with not enough volumes, and handed off to BJ to delete.

<div style="text-align: right"> — SC </div>

---

As we developed and discussed formalization of directory structures and `cubids`, BJ copied data to `/cbica/projects/RBC/HBN/bidsdatasets/`.

\#TODO SC & BJ was this where datalad was initialised?

BJ received from SC a CSV of 16 DWI scans in HBN with volume count mismatch. The scans were deleted from the dataset using a simple `rm -rf` command.

It was decided that 3mins is the cutoff for BOLD scans. So incomplete scans are scans that lasted less than 3mins. In HBN, this differed based off of the type of sessions that were conducted:
- For scans in the Site-SI sessions, the TR is 2.4s, and so 3 mins is 75 volumes. Any scan with the Site-SI session and less than 75 volumes was deleted.
- For all other session types, TR is 0.8s, so 3 mins is 225 volumes. Any scan from a session that was not Site-SI and less than 225 volumes was deleted.
- Task-PEER is a short task, and therefore, will last less than the cutoff time. Scans that met the above criterion but were within the PEER task were not deleted.

Similarly, DWI scans were purged of incomplete scans. Each full DWI run with less than a total of 64 volumes (32 volumes per scan) was deleted. Therefore, if a scan was identified with less than 32 volumes, then this scan and its counterpart that completed the DWI run was deleted. The scans that did not meet the cutoff were identified by:
- Running `cubids-validate` on the dataset and working through the validation errors
- Running `cubids-group` on the dataset and using the summary and files CSVs to identify the scans with volumes that do not meet the cutoff.

In order to delete the scans from the dataset being used, a branch titled `incomplete_scans` was created where the full HBN dataset exists. Scans were deleted solely from the `master` branch. As such, a copy of the dataset exists without any deletions for anyone who may need these scans.

In initial iterations, these scans were deleted using an independent deletion script that can still be found at `/cbica/project/RBC/HBN/code/deletion.py`. The script loops over a list of paths to the scans that did not meet the cutoff described above and deletes them from the dataset. The deletion script, prior to its final iteration available on CUBIC, caused errors in the BIDS validation. This resulted in having to re-do the above process from scratch.

\#TODO BJ where does the re-do begin from?

The final iteration available is a functional script, however, the informatics team decided it would be best to include a purge function into `CuBIDS` in order simplify and standardize the curation process.
The deletion for these scans was completed using the `CuBIDS-purge` function.

SYDNEY 
Working off the copy of HBN at ~/RBC_RAWDATA/bidsdatasets/HBN, we checked out an includes-incompletes branch and then purged 16 dwi scans that were receiving a VOLUME_COUNT_MISMATCH warning during validation along with 16 bold scans with less than 3 mins of data from the main branch. See below for the list. 

/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARWE130JMG/ses-HBNsiteRU/dwi/sub-NDARWE130JMG_ses-HBNsiteRU_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARVP285RXV/ses-HBNsiteRU/dwi/sub-NDARVP285RXV_ses-HBNsiteRU_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARBR128UFP/ses-HBNsiteCBIC/dwi/sub-NDARBR128UFP_ses-HBNsiteCBIC_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARGK253TTG/ses-HBNsiteRU/dwi/sub-NDARGK253TTG_ses-HBNsiteRU_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARLY872ZXA/ses-HBNsiteRU/dwi/sub-NDARLY872ZXA_ses-HBNsiteRU_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARFG568PXZ/ses-HBNsiteRU/dwi/sub-NDARFG568PXZ_ses-HBNsiteRU_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARZW662UK6/ses-HBNsiteRU/dwi/sub-NDARZW662UK6_ses-HBNsiteRU_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARRU499DP2/ses-HBNsiteRU/dwi/sub-NDARRU499DP2_ses-HBNsiteRU_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDAREC078VFT/ses-HBNsiteRU/dwi/sub-NDAREC078VFT_ses-HBNsiteRU_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARRK038CBD/ses-HBNsiteCBIC/dwi/sub-NDARRK038CBD_ses-HBNsiteCBIC_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARWK051GG4/ses-HBNsiteRU/dwi/sub-NDARWK051GG4_ses-HBNsiteRU_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARLB671TLU/ses-HBNsiteRU/dwi/sub-NDARLB671TLU_ses-HBNsiteRU_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARJZ167VEZ/ses-HBNsiteCBIC/dwi/sub-NDARJZ167VEZ_ses-HBNsiteCBIC_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARYF272EDC/ses-HBNsiteCBIC/dwi/sub-NDARYF272EDC_ses-HBNsiteCBIC_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARYZ906UHJ/ses-HBNsiteRU/dwi/sub-NDARYZ906UHJ_ses-HBNsiteRU_acq-64dir_dwi.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARBM490LK7/ses-HBNsiteRU/dwi/sub-NDARBM490LK7_ses-HBNsiteRU_acq-64dir_dwi.nii.gz


/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDAREG930XPP/ses-HBNsiteCBIC/func/sub-NDAREG930XPP_ses-HBNsiteCBIC_task-movieTP_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARRA719CPH/ses-HBNsiteCBIC/func/sub-NDARRA719CPH_ses-HBNsiteCBIC_task-movieTP_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARZH930XTP/ses-HBNsiteCBIC/func/sub-NDARZH930XTP_ses-HBNsiteCBIC_task-movieTP_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARCH868WVX/ses-HBNsiteRU/func/sub-NDARCH868WVX_ses-HBNsiteRU_task-rest_run-1_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARKA946MJ1/ses-HBNsiteRU/func/sub-NDARKA946MJ1_ses-HBNsiteRU_task-rest_run-1_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARRM725BRV/ses-HBNsiteCUNY/func/sub-NDARRM725BRV_ses-HBNsiteCUNY_task-rest_run-1_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARTB003FDD/ses-HBNsiteCUNY/func/sub-NDARTB003FDD_ses-HBNsiteCUNY_task-rest_run-1_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARXB286YBR/ses-HBNsiteRU/func/sub-NDARXB286YBR_ses-HBNsiteRU_task-rest_run-1_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARVB538ZGJ/ses-HBNsiteRU/func/sub-NDARVB538ZGJ_ses-HBNsiteRU_task-movieDM_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARYL443NG6/ses-HBNsiteCUNY/func/sub-NDARYL443NG6_ses-HBNsiteCUNY_task-movieDM_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARNF994TPA/ses-HBNsiteRU/func/sub-NDARNF994TPA_ses-HBNsiteRU_task-movieDM_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARJJ413MNH/ses-HBNsiteRU/func/sub-NDARJJ413MNH_ses-HBNsiteRU_task-movieDM_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARGJ627BL2/ses-HBNsiteRU/func/sub-NDARGJ627BL2_ses-HBNsiteRU_task-movieDM_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARET332CTB/ses-HBNsiteRU/func/sub-NDARET332CTB_ses-HBNsiteRU_task-movieDM_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARZH930XTP/ses-HBNsiteCBIC/func/sub-NDARZH930XTP_ses-HBNsiteCBIC_task-movieDM_bold.nii.gz
/cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/HBN/sub-NDARET949LMU/ses-HBNsiteSI/func/sub-NDARET949LMU_ses-HBNsiteSI_task-rest_bold.nii.gz

We checked out a branch called no-T2s. Then, Lei then merged the defaced, non skull-stripped T2w scans he had stored in a separate directory on cubic into the main branch and uploaded the 6 T1w sidecars we identified as missing. We then ran add-nifti-info to add nifti information from the sidecars Lei added (all T2ws and 6 T1ws). 

We identified 7 anat/ scans (2 T2ws and 5 T1ws) with a very low Dimension 1 Size (between 20 and 32 voxels). We decided to purge these scans. 
