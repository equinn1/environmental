# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 09:47:26 2016

@author: gquinn
"""
import pickle
from counting_process_classes import *

subjects={}                                       #subject dictionary

for dis in ['BDD','MDD','OCD','SOC']:
    fname="data/STATE_"+dis+".txt"

    fp = open(fname,'r')   #read state changes

    for line in fp:                              #loop through line by line
        if("SS:" in line):                            #first entry for this S
            wds = line.split()
            SS=wds[0].split(":")[1]                   #subject number
            initline=line

        
        if("ID" in line):                             #ID line
            wl=line.split("=")
            if(len(wl)>1):                            #skip if no ID
                ID=wl[1]                          #save ID if there is one
                if(ID in subjects.keys()):            #ID already present?
                    newsub=subjects[ID]
                else:
                    newsub=subj(ID,SS)                #call subject constructor
                    subjects[ID]=newsub
            
        if("Initial" in line):                        #save initial status
            init_state=line.split()[2]
            newsub.set_intake_state(init_state,dis)
            scentries=[]
            newsc=scentry(0,None,init_state)
            scentries.append(newsc)
            newsub.set_scentries(scentries,dis)
        
            
        if("Max" in line):
            maxtime=line.split()[2]
            newsub.set_maxtime(maxtime)
            scentries=newsub.get_scentries(dis)
            lastone=len(scentries)-1
            lastcp=scentries[lastone]
            lastcp.set_end(maxtime)
            newsub.set_scentries(scentries,dis)

        if("STATE CHANGE" in line):
            wds=line.split()
            from_state=wds[3]
            to_state=wds[5]
            week=wds[8]
            newsc=scentry(week,None,to_state)
            scentries=newsub.get_scentries(dis)
            imax=len(scentries)-1
            sce = scentries[imax]
            sce.set_end(week)
            scentries.append(newsc)
            newsub.set_scentries(scentries,dis)

print("Starting list")
for key in subjects:
    print(subjects[key].get_ID())
    scdict=subjects[key].get_cpdict()
    for dis in scdict.keys():
        scentries=scdict[dis]
        for i in range(0,len(scentries)):
            sce = scentries[i]
            start=sce.get_start()
            end=sce.get_end()
            state=sce.get_state()
            print "%d %s %s %s" % (i, start, end, state)
        
pf=open('bdd_state_python.obj','wb')      
pickle.dump(subjects,pf,pickle.HIGHEST_PROTOCOL)