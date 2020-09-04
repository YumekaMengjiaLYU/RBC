Transfer: Various scripts used to transfer data from PNC to the RBC project; asynchronous

Refacer: Docker wrapper + CLI for `afni_refacer`

Validation: Tracking of BIDS data validation

To check the status of validation, go to `RBC/PennLINC/Validation/<PROJECT_NAME>/`. Importantly, the file `output_status.csv` lists which subjects output data from Flywheel successfully, while the files `validation.json` and `validation.csv` are output and parsed output of the BIDS validator.