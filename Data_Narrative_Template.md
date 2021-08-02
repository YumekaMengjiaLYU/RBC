## Data Narrative for [INSERT DATASET NAME HERE]

### Important Links (should all be on GitHub):
* Data Processing Flow Diagram:
   * Flow diagram that describes the lifecycle of this dataset 
* Curation/Validation DSR:
   * GitHub projects page that helps you track the curation and validation portion of the dataset. This page should be updated every time you perform an action on the data. 
* Containerized Pipeline Testing Queue/Status Report: 
   * GitHub projects page that helps you track the progress of containerized pipeline runs on the data. 
   
### Plan for the Data 

* Why does PennLINC need this data?
* For which project(s) is it intended? Please link to project pages below:
* What is our goal data format?
   * i.e. in what form do we want the data by the end of the "Curation" step? BIDS? Something else? 

### Data Acquisition

* Who is responsible for acquiring this data?
* Do you have a DUA? Who is allowed to access the data?
* Where was the data acquired? 
* Describe the data. What type of information do we have? Things to specify include:
   * number of subjects
   * types of images
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
* Path to curation scripts/heurstics: 
* Path to final CuBIDS csvs: 
* Describe the Validation Process. Include a list of the initial and final errors and warnings.
* Describe additions, deletions, and metadata changes (if any).

### Preprocessing Pipelines 
* For each pipeline (e.g. QSIPrep, fMRIPrep, XCP, C-PAC), please fill out the following information:
   * Pipeline Name: 
   * Who is responsible for running preprocessing pipelines/audits on this data?
   * Where are you running these pipelines? CUBIC? PMACS? Somewhere else?
   * Did you implement exemplar testing? If so, please fill out the information below:
      * Path to exemplar dataset:
      * Path to exemplar outputs:
      * Path to exemplar audit:
    * For production testing, please fill out the information below:
      * Path to production inputs:
      * Path to production outputs:
      * Path to production audit: 

### Post Processing 

* Who is using the data/for which projects are people in the lab using this data?
   * Link to project page(s) here  
* List all analyses that have been run on this data:
* Did you use pennlinckit?
   * https://github.com/PennLINC/PennLINC-Kit/tree/main/pennlinckit  
