import flywheel


allsub='sub-NDARAD703XA2_sub-NDARAP739AUP_sub-NDARAU939WUK_sub-NDARGH634ME7_sub-NDARLN550RM6_sub-NDARNY894TH7_sub-NDARRP008LJ6_sub-NDARUP908XUJ_'

allsub='sub-NDARKX528PH3'
###############
idx=0
for project in fw.projects():
    print('%s: %s' % (project.id, project.label))
    if project.label != 'RBC_HBN':
        continue

    for subject in project.subjects():
        #if subject.label == 'sub-NDARFR820KFF':
        #if "sub-NDAR" in subject.label:
        if subject.label in allsub:

            print('%s: %s' % (subject.id, subject.label))
            idx += 1
            for session in subject.sessions():
                print('%s: %s' % (session.id, session.label))
                bb=fw.get_session(session.id).acquisitions()
                for k in range(0,len(bb)):
                    for j in range(0,len(bb[k].files)):
                        acq_object = fw.get(bb[k].id)
                        info=bb[k].files[j]['info']['BIDS']
                        info['Filename']=bb[k].files[j].name
                        acq_object.update_file_info(bb[k].files[j].name,{'BIDS':info})

