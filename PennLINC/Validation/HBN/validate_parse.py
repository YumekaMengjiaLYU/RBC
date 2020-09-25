import sys
import os
import logging
import subprocess as sub
import pandas as pd
from fw_heudiconv.cli.validate import validate_local
from fw_heudiconv.backend_funcs.convert import parse_validator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('fw-heudiconv-validator')


def main():

    args = sys.argv
    validate_local(args[1] + '/bids_directory', True, tabulate = args[1])
    
    df = parse_validator(args[1] + '/issues.json')
    df.to_csv(args[1] + '/issues.csv')
    
if __name__ == "__main__":
    main()