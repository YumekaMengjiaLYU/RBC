## Data Narrative for Chinese Color Nest Project (CCNP)

### Important Links (should all be on GitHub):
* Data Processing Flow Diagram:
   * https://github.com/PennLINC/RBC/blob/master/PennLINC/CCNP_BIDS_Fix/participation.drawio   
      * Flow diagram that describes the lifecycle of this dataset 
* DSR GitHub Project Page(Curation/Validation and Processing Queue Status):
   * https://github.com/PennLINC/RBC/blob/master/PennLINC/RBC_Dataset_Status_Report.txt
      * Cards for tracking the curation and validation portion of the dataset. This page should be updated every time you perform an action on the data. 
      * Cards for tracking the progress of containerized pipeline runs on the data. 
   
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
* From where was the data downloaded?
* Where is it currently being stored?
* What form is the data in upon intial download (DICOMS, NIFTIS, something else?)
* Are you using Datalad? 
* Is the data backed up in a second location? If so, please provide the path to the backup location:


### Curation Process

* Who is responsible for curating this data?
* GitHub Link to curation scripts/heurstics: 
* GitHub Link to final CuBIDS csvs: 
* Describe the Validation Process. Include a list of the initial and final errors and warnings.
* Describe additions, deletions, and metadata changes (if any).

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
      * Path to production inputs: /cbica/projects/RBC/RBC_
      * GitHub Link to production outputs:
      * GitHub Link to production audit: 
 * Pipeline Name: XCP
   * Who is responsible for running preprocessing pipelines/audits on this data: Max Bertolero 
   * Where are you running these pipelines: CUBIC 
   * Did you implement exemplar testing: No
      * Path to exemplar dataset: /cbica/projects/RBC/RBC_EXEMPLARS/ccnp_exemplars 
      * Path to exemplar outputs: 
      * GitHub Link to exemplar audit: 
    * For production testing, please fill out the information below:
      * Path to production inputs: /cbica/projects/RBC/RBC_
      * GitHub Link to production outputs:
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
