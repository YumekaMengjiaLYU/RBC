#!/usr/bin/env python
# coding: utf-8

# Setting up the validator:

# In[1]:


import flywheel
import os
from pathlib import Path

client = flywheel.Client()


# In[2]:


nki = client.projects.find_first("label=RBC_NKI")
pnc = client.projects.find_first("label=RBC_PNC")
hbn = client.projects.find_first("label=RBC_HBN")


# In[3]:


nki_subjects = [x.label for x in nki.subjects()]
pnc_subjects = [x.label for x in pnc.subjects()]
hbn_subjects = [x.label for x in hbn.subjects()]


# In[32]:


import subprocess
import multiprocessing as mp


num = 12  # set to the number of workers you want (it defaults to the cpu count of your machine)


# In[45]:


def validate(project, subject, test=True):
    path = '/storage/ttapera/RBC/data/validation/{}/{}'.format(project, subject)
    call = 'fw-heudiconv-validate --flywheel --project RBC_{} --subject {} --directory {} --tabulate {}'.format(project, subject, path, path)
    if test:
        call = 'echo ' + call
    proc = subprocess.check_call(call,shell=True, stdout=subprocess.PIPE)
    return proc

    


# In[48]:


import multiprocessing as mp
pool = mp.Pool(processes=12)


# In[49]:


for subject in nki_subjects:
    pool.apply_async(validate, ('NKI',subject,False))
    
pool.close()
pool.join()


# In[57]:


pool = mp.Pool(processes=16)


# In[ ]:


for subject in pnc_subjects:
    pool.apply_async(validate, ('PNC',subject,False))
    
pool.close()
pool.join()


# In[ ]:


pool = mp.Pool(processes=16)


# In[ ]:


for subject in hbn_subjects:
    pool.apply_async(validate, ('HBN',subject,False))
    
pool.close()
pool.join()

