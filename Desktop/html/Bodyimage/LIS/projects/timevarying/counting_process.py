# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 09:47:26 2016

@author: gquinn
"""
import pickle
from counting_process_classes import *
        
fp = open('../fouryear/data/STATE_BDD.txt','r')   #read state changes

subjects={}                                       #subject dictionary
linect=0
for line in fp:                                   #loop through line by line
    linect=linect+1
    if("SS:" in line):                            #first entry for this S
        wds = line.split()
        SS=wds[0].split(":")[1]                   #subject number
        scd102=wds[2]                             #BDD intake status
        scd104=wds[4]
        scd106=wds[6]

        
    if("ID" in line):                             #ID line
        wl=line.split("=")
        if(len(wl)>1):                            #skip if no ID
            ID=wl[1]                              #save ID if there is one
            
    if("Initial" in line):                        #save initial status
        init_state=line.split()[2]
        newsub=subj(ID,SS,scd102,scd104,scd106)
        cpentries=[]
        cpent=cpentry(0,None,init_state)
        cpentries.append(cpent)
            
    if("Max" in line):
        maxwk=line.split()[2]
        newsub.set_maxwk(maxwk)
        lastone=len(cpentries)-1
        lastcp=cpentries[lastone]
        lastcp.set_end(maxwk)
        newsub.set_cpentries(cpentries)
        if(ID != None):
            subjects[ID]=newsub

        print(ID)
        
    if("STATE CHANGE" in line):
        wds=line.split()
        from_state=wds[3]
        to_state=wds[5]
        week=wds[8]
        imax=len(cpentries)-1
        cpe = cpentries[imax]
        cpe.set_end(week)
        newcp=cpentry(week,None,to_state)
        print(len(cpentries))
        cpentries.append(newcp)
        print(len(cpentries))
        print(week)

print("Starting list")
for key in subjects:
    print(subjects[key].get_ID())
    cpentries=subjects[key].get_cpentries()
    for i in range(0,len(cpentries)):
        cpe = cpentries[i]
        start=cpe.get_start()
        end=cpe.get_end()
        state=cpe.get_state()
        print "%d %s %s %s" % (i, start, end, state)
        
pf=open('bdd_state_python.obj','w')      
pickle.dump(subjects,pf,pickle.HIGHEST_PROTOCOL)