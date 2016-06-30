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
            cpentries=[]
            newcp=cpentry(0,None,init_state)
            cpentries.append(newcp)
            newsub.set_cpentries(cpentries,dis)
        
            
        if("Max" in line):
            maxtime=line.split()[2]
            newsub.set_maxtime(maxtime)
            cpentries=newsub.get_cpentries(dis)
            lastone=len(cpentries)-1
            lastcp=cpentries[lastone]
            lastcp.set_end(maxtime)
            newsub.set_cpentries(cpentries,dis)

        if("STATE CHANGE" in line):
            wds=line.split()
            from_state=wds[3]
            to_state=wds[5]
            week=wds[8]
            newcp=cpentry(week,None,to_state)
            cpentries=newsub.get_cpentries(dis)
            imax=len(cpentries)-1
            cpe = cpentries[imax]
            cpe.set_end(week)
            cpentries.append(newcp)
            newsub.set_cpentries(cpentries,dis)

print("Starting list")
for key in subjects:
    print(subjects[key].get_ID())
    cpdict=subjects[key].get_cpdict()
    for dis in cpdict.keys():
        cpentries=cpdict[dis]
        for i in range(0,len(cpentries)):
            cpe = cpentries[i]
            start=cpe.get_start()
            end=cpe.get_end()
            state=cpe.get_state()
            print "%d %s %s %s" % (i, start, end, state)
        
pf=open('bdd_state_python.obj','wb')      
pickle.dump(subjects,pf,pickle.HIGHEST_PROTOCOL)