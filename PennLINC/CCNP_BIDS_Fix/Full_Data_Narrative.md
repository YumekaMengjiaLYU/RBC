## Data Narrative for Chinese Color Nest Project (CCNP)

### Important Links (should all be on GitHub):
* Data Processing Flow Diagram:
   * https://github.com/PennLINC/RBC/blob/master/PennLINC/CCNP_BIDS_Fix/participation.drawio   
      * Flow diagram that describes the lifecycle of this dataset 
* DSR for Curation/Validation:
   * https://github.com/PennLINC/RBC/blob/master/PennLINC/RBC_Dataset_Status_Report.txt
      * Doc tracking the curation and validation portion of the dataset. This page should be updated every time you perform an action on the data. 
   * https://github.com/PennLINC/RBC/projects/1?add_cards_query=is%3Aopen
      * Doc tracking the progress of containerized pipeline runs on the data. 
   
### Plan for the Data 

* Why does PennLINC need this data?
  * CCNP is part of the Reproducible Brain Chart (RBC) data collection initiative.  
* For which project(s) is it intended? Please link to project pages below: 
* What is our goal data format by the end of curation?
   * BIDS (niftis + sidecars)

### Data Acquisition

* Who is responsible for acquiring this data?
  * Haoming Dong (Beijing Normal University) and Zhe Zhang (Chinese Academy of Sciences)
* Do you have a DUA? Who is allowed to access the data?
* Where was the data acquired? 
  * Beijing Normal University 
* Describe the data. What type of information do we have? Things to specify include:
   * number of subjects: 195
   * types of images: T1ws (anat) and task-rest (func)
   * demographic data
   * clinical/cognitive data
   * any canned QC data
   * any preprocessed or derived data

### Download and Storage 

* Who is responsible for downloading this data?
  * Sydney Covitz 
* From where was the data downloaded?
  * Data was emailed to PennLINC from Haoming Dong. 
* Is the data checked into Datalad, and if so, is it absent of PHI?
  * Yes, and yes
* Where is it currently being stored?
  * CCNP is a Datalad Dataset on CUBIC 
    * CUBIC PATH: /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/CCNP 
* Is the data backed up in a second location? If so, please provide the path to the backup location:
  * Yes. CCNP has a sibling (backup copy) on PMACS
    * RIA Store Path: ssh://sciget.pmacs.upenn.edu/project/RBC/RIA/BIDS/970/4eab1-3320-41f0-9fce-3c6961b4ac96
* In what form did PennLINC receive the data (DICOMS, NIFTIS, something else)?
  * NIFTIS and Sidecars 

### Curation Process

* Who is responsible for curating this data?
  * Sydney Covitz  
* GitHub Link to curation scripts/heurstics: 
* GitHub Link to final CuBIDS csvs: https://github.com/PennLINC/RBC/tree/master/PennLINC/CCNP_BIDS_Fix 
* Describe the Validation Process. Include a list of the initial and final errors and warnings.
  * CCNP was BIDS Valid when it was given to us.  
* Describe additions, deletions, and metadata changes (if any).
  * CCNP was given to us in a fairly clean state with bids validation passing. After checking the dataset into datalad, we used cubids-add-nifti-info to add volume number, obliquity, and voxel size infomration to each sidecar in the dataset. We were initially missing two subjects' T1w scans. Haoming Dong sent them to us over email once we realized they were missing. Additionally we removed a single bold scan, sub-colornest035/ses-1/func/sub-colornest035_ses-1_task-rest_run-02_bold.nii.gz, due to the fac that it has a PhaseEncodingDirectoin (PED) of "i." Run-01 of sub-colornest035's rest scan remains in the dataset and has the correct PED. 
 * See the Datalad commit history below for a summary of changes that were made to this dataset  
    * 2d542bc (HEAD -> master, PMACS/master) Saving bond-apply changes with clustering
    * 4439f96 added 0 to MergeInto column of param group with PhaseEncodingDirection of i, so 1 scan and 1 json got deleted
    * 5bfbf37 added nifti info to sidecars for sub-colornest115 and sub-colornest181 T1s
    * f0d34d9 added T1s and their sidecars for sub-colornest115 and sub-colornest181
    * 9fa29e4 Added nifti info to sidecars
    * 0fbffc1 [DATALAD] new dataset
    * d4ee651 Instruct annex to add text files to Git
    * 3563f23 add bids data
    * e5230f1 [DATALAD] new dataset

### Preprocessing Pipelines 
* For each pipeline (e.g. QSIPrep, fMRIPrep, XCP, C-PAC), please fill out the following information:
   * Pipeline Name: fMRIPrep
   * Who is responsible for running preprocessing pipelines/audits on this data: Sydney Covitz
   * Where are you running these pipelines: CUBIC 
   * Did you implement exemplar testing: Yes
      * Path to exemplar dataset: /cbica/projects/RBC/RBC_EXEMPLARS/ccnp_exemplars 
      * Path to exemplar outputs: 
      * GitHub Link to exemplar audit: 
    * For production testing, please fill out the information below:
      * Path to production inputs: /cbica/projects/RBC/RBC_RAWDATA/bidsdatasets/CCNP
      * GitHub Link to production outputs:
      * GitHub Link to production audit: 
 * Pipeline Name: XCP
   * Who is responsible for running preprocessing pipelines/audits on this data: Max Bertolero 
   * Where are you running these pipelines: CUBIC 
   * Did you implement exemplar testing: No
      * Path to exemplar dataset: /cbica/projects/RBC/RBC_EXEMPLARS/ccnp_exemplars 
      * Path to exemplar outputs: /cbica/projects/RBC/testing/ccnp_f3
      * GitHub Link to exemplar audit: 
    * For production testing, please fill out the information below:
      * Path to production inputs: /cbica/projects/RBC/RBC_RBC_EXEMPLARS/ccnp_exemplars 
      * GitHub Link to production outputs: ~/cbica/projects?RBC/
      * GitHub Link to production audit: 

### Post Processing 

* Who is using the data/for which projects are people in the lab using this data?
   * Link to project page(s) here  
* For each post-processing analysis that has been run on this data, fill out the following
   * Who performed the analysis?
   * Where it was performed (CUBIC, PMACS, somewhere else)?
   * GitHub Link(s) to result(s)
   * Did you use pennlinckit?  
      * https://github.com/PennLINC/PennLINC-Kit/tree/main/pennlinckit  
