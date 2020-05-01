import flywheel
import re
import sys
import pandas as pd

DEBUG = True

# get the penn_ids list
penn_ids = pd.read_csv(sys.argv[1], dtype = {'bblid': str, 'reid': str})

penn_ids['sub_id'] = 'sub-' + penn_ids['reid']

if DEBUG:
    print(penn_ids)

client = flywheel.Client()

RBC_proj = client.projects.find_first('label="ReproBrainChart"')

RBC_subjects = RBC_proj.subjects()

PNC_CS_proj = client.projects.find_first('label="PNC_CS_810336"')
PNC_LG_proj = client.projects.find_first('label="PNC_LG_810336"')

PNC_CS_subjects = PNC_CS_proj.subjects()
PNC_LG_subjects = PNC_LG_proj.subjects()




# function to remove a subject from the project
def remove_current_rbc_subject(row, RBC_subjects):

    target = [x for x in RBC_subjects if x.label == row['sub_id']]
    if len(target) == 1:
        print('found subject to remove: ', target[0].id)
        print('client.delete_subject(target[0].id)')




for index, row in penn_ids.iloc[:5,].iterrows():
    remove_current_rbc_subject(row, RBC_subjects)


